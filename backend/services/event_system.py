"""
事件系统
管理随机事件的触发和应用
"""

import random
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Any
from datetime import datetime


@dataclass
class GameEvent:
    """游戏事件类 (支持新格式)"""
    
    id: str
    name: str
    description: str
    name_en: str = ""  # 英文名称
    event_type: str = "economic"  # economic, business, negative, government, market, technology, human_resource, marketing, infrastructure
    rarity: str = "common"  # common, uncommon, rare, epic, legendary
    effects: Dict[str, Any] = field(default_factory=dict)  # 效果字典
    duration: int = 0  # 持续天数 (-1=永久，0=立即)
    trigger_condition: str = "random"  # 触发条件
    weight: int = 10  # 权重
    
    # 旧格式兼容字段
    impact: Dict[str, float] = field(default_factory=dict)
    probability: float = 1.0
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "description": self.description,
            "type": self.event_type,
            "rarity": self.rarity,
            "effects": self.effects,
            "duration": self.duration,
            "trigger_condition": self.trigger_condition,
            "weight": self.weight,
        }
    
    def apply(self, company) -> dict:
        """
        应用事件效果
        返回应用结果
        """
        result = {
            "event_id": self.id,
            "event_name": self.name,
            "applied_effects": [],
            "messages": [],
        }
        
        # 应用效果 (新格式)
        for effect_key, effect_value in self.effects.items():
            # 处理一次性收入
            if effect_key == "oneTimeIncome":
                company.cash += effect_value
                company.total_earnings += effect_value
                result["applied_effects"].append(f"+${effect_value} cash")
                result["messages"].append(f"获得一次性收入 ${effect_value}")
            
            # 处理声誉
            elif effect_key == "reputation":
                if isinstance(effect_value, (int, float)):
                    if effect_value > 0:
                        company.reputation = min(5.0, company.reputation + effect_value / 100)
                    else:
                        company.reputation = max(0.0, company.reputation + effect_value / 100)
                    result["applied_effects"].append(f"{effect_value:+} reputation")
            
            # 处理倍数效果 (需要特殊处理的属性)
            elif isinstance(effect_value, (int, float)):
                # 存储倍数效果供游戏系统使用
                if not hasattr(company, 'active_effects'):
                    company.active_effects = {}
                
                if self.duration == -1:  # 永久效果
                    company.active_effects[effect_key] = effect_value
                elif self.duration > 0:  # 临时效果
                    if effect_key not in company.active_effects:
                        company.active_effects[effect_key] = []
                    company.active_effects[effect_key].append({
                        "value": effect_value,
                        "expires_day": company.day + self.duration,
                    })
                
                result["applied_effects"].append(f"{effect_key}: {effect_value}x")
        
        # 旧格式兼容
        for stat, value in self.impact.items():
            if hasattr(company, stat):
                current = getattr(company, stat)
                if isinstance(current, (int, float)):
                    setattr(company, stat, current + value)
                    result["applied_effects"].append(f"{stat}: {value:+}")
        
        return result
    
    def check_trigger(self, company) -> bool:
        """
        检查是否满足触发条件
        """
        if self.trigger_condition == "random":
            return True
        
        # 解析条件 (简单实现)
        try:
            # 支持的条件格式："reputation >= 50", "capital >= 100000", "marketShare > 0.3"
            condition = self.trigger_condition
            
            # 映射属性名
            attr_map = {
                "reputation": company.reputation,
                "capital": company.cash,
                "marketShare": 0.5,  # 简化处理
                "brandValue": 100,  # 简化处理
                "techLevel": len(company.technologies),
                "qualityControl": 70,  # 简化处理
                "marketingBudget": 10000,  # 简化处理
                "inventory": 50,  # 简化处理
                "maxCapacity": 100,  # 简化处理
                "securityLevel": 80,  # 简化处理
            }
            
            # 简单评估条件
            for attr, value in attr_map.items():
                condition = condition.replace(attr, str(value))
            
            # 安全评估
            return eval(condition)
        except:
            return False
    
    @classmethod
    def from_dict(cls, data: dict) -> "GameEvent":
        """从字典创建事件 (支持新格式)"""
        return cls(
            id=data.get("id", "unknown"),
            name=data.get("name", "未知事件"),
            name_en=data.get("nameEn", ""),
            description=data.get("description", ""),
            event_type=data.get("type", data.get("event_type", "economic")),
            rarity=data.get("rarity", "common"),
            effects=data.get("effects", {}),
            duration=data.get("duration", 0),
            trigger_condition=data.get("triggerCondition", data.get("trigger_condition", "random")),
            weight=data.get("weight", 10),
            # 旧格式兼容
            impact=data.get("impact", {}),
            probability=data.get("probability", 1.0),
        )


class EventSystem:
    """事件系统类"""
    
    def __init__(self, events_file: Optional[str] = None):
        self.active_events: List[GameEvent] = []
        self.event_history: List[GameEvent] = []
        self.event_pool: List[GameEvent] = []
        self.rarity_weights: Dict[str, int] = {
            "common": 15,
            "uncommon": 10,
            "rare": 6,
            "epic": 3,
            "legendary": 1,
        }
        
        # 加载事件文件
        if events_file:
            self.load_events_from_file(events_file)
        else:
            # 尝试默认路径
            default_path = Path(__file__).parent.parent / "data" / "events.json"
            if default_path.exists():
                self.load_events_from_file(str(default_path))
    
    def load_events_from_file(self, file_path: str) -> bool:
        """
        从 JSON 文件加载事件
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            events_data = data.get("events", [])
            self.event_pool = [GameEvent.from_dict(evt) for evt in events_data]
            
            # 加载稀有度配置
            if "rarityLevels" in data:
                for rarity, config in data["rarityLevels"].items():
                    if "weight" in config:
                        self.rarity_weights[rarity] = config["weight"]
            
            print(f"[EventSystem] 成功加载 {len(self.event_pool)} 个事件")
            return True
        except Exception as e:
            print(f"[EventSystem] 加载事件文件失败：{e}")
            return False
    
    def trigger_random_event(self, company=None) -> Optional[GameEvent]:
        """触发随机事件"""
        if not self.event_pool:
            return None
        
        # 过滤可触发的事件
        available_events = []
        for event in self.event_pool:
            if event.check_trigger(company):
                available_events.append(event)
        
        if not available_events:
            return None
        
        # 按稀有度权重选择
        selected_event = self._weighted_random_by_rarity(available_events)
        
        if selected_event:
            self.event_history.append(selected_event)
            
            # 如果是临时事件，加入活跃事件列表
            if selected_event.duration > 0:
                self.active_events.append(selected_event)
        
        return selected_event
    
    def _weighted_random_by_rarity(self, events: List[GameEvent]) -> Optional[GameEvent]:
        """按稀有度权重随机选择事件"""
        if not events:
            return None
        
        # 计算总权重
        total_weight = sum(self.rarity_weights.get(e.rarity, 10) for e in events)
        if total_weight == 0:
            return random.choice(events)
        
        # 随机选择
        roll = random.random() * total_weight
        cumulative = 0
        
        for event in events:
            cumulative += self.rarity_weights.get(event.rarity, 10)
            if roll <= cumulative:
                return event
        
        return events[-1]
    
    def update_active_events(self, company) -> List[dict]:
        """
        更新活跃事件 (处理过期事件)
        返回过期事件列表
        """
        expired = []
        current_day = company.day if company else 0
        
        # 清理过期事件
        remaining_events = []
        for event in self.active_events:
            if event.duration > 0:
                # 检查是否过期 (简化处理)
                if len(self.event_history) > 0 and event in self.event_history:
                    event_index = self.event_history.index(event)
                    days_active = len(self.event_history) - event_index
                    if days_active >= event.duration:
                        expired.append(event.to_dict())
                        continue
            remaining_events.append(event)
        
        self.active_events = remaining_events
        return expired
    
    def get_event_history(self, limit: int = 10) -> List[dict]:
        """获取事件历史"""
        return [e.to_dict() for e in self.event_history[-limit:]]
    
    def get_active_events(self) -> List[dict]:
        """获取当前活跃事件"""
        return [e.to_dict() for e in self.active_events]


# 全局事件系统实例
_global_event_system: Optional[EventSystem] = None


def get_event_system() -> EventSystem:
    """获取全局事件系统实例"""
    global _global_event_system
    if _global_event_system is None:
        _global_event_system = EventSystem()
    return _global_event_system


def reset_event_system(events_file: Optional[str] = None) -> EventSystem:
    """重置事件系统实例"""
    global _global_event_system
    _global_event_system = EventSystem(events_file)
    return _global_event_system
