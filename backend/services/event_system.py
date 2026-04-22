"""
事件系统
管理随机事件的触发和应用
"""

import random
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional
from datetime import datetime


@dataclass
class GameEvent:
    """游戏事件类"""
    
    id: str
    name: str
    description: str
    event_type: str  # positive, negative, neutral
    impact: Dict[str, float]  # 影响 {cash: 1000, reputation: 0.1, ...}
    duration: int = 0  # 持续天数 (0=立即)
    probability: float = 1.0  # 触发概率
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.event_type,
            "impact": self.impact,
            "duration": self.duration,
        }
    
    def apply(self, company) -> None:
        """应用事件效果"""
        for stat, value in self.impact.items():
            if hasattr(company, stat):
                current = getattr(company, stat)
                if isinstance(current, (int, float)):
                    setattr(company, stat, current + value)


class EventSystem:
    """事件系统类"""
    
    def __init__(self):
        self.active_events: List[GameEvent] = []
        self.event_history: List[GameEvent] = []
    
    def trigger_random_event(self) -> Optional[GameEvent]:
        """触发随机事件"""
        roll = random.random()
        
        # 30% 概率正面事件
        if roll < 0.30:
            event = self._get_positive_event()
        # 20% 概率负面事件
        elif roll < 0.50:
            event = self._get_negative_event()
        # 50% 概率无事件
        else:
            return None
        
        if event:
            self.event_history.append(event)
            return event
        
        return None
    
    def _get_positive_event(self) -> Optional[GameEvent]:
        """获取正面事件"""
        events = [
            GameEvent(
                id="client_tip",
                name="客户给小费",
                description="客户对项目非常满意，给了额外小费",
                event_type="positive",
                impact={"cash": 5000},
                probability=0.10,
            ),
            GameEvent(
                id="agent_inspiration",
                name="Agent 灵感爆发",
                description="某个 Agent 突然灵感爆发，工作效率翻倍",
                event_type="positive",
                impact={},  # 特殊处理
                probability=0.05,
            ),
            GameEvent(
                id="tech_breakthrough",
                name="技术突破",
                description="团队实现了技术突破",
                event_type="positive",
                impact={"reputation": 0.2},
                probability=0.05,
            ),
            GameEvent(
                id="viral_marketing",
                name="病毒式传播",
                description="公司在社交媒体上走红",
                event_type="positive",
                impact={"reputation": 0.3},
                probability=0.05,
            ),
            GameEvent(
                id="government_grant",
                name="政府补贴",
                description="获得政府创业补贴",
                event_type="positive",
                impact={"cash": 10000},
                probability=0.05,
            ),
        ]
        
        # 根据概率加权随机选择
        return self._weighted_random_choice(events)
    
    def _get_negative_event(self) -> Optional[GameEvent]:
        """获取负面事件"""
        events = [
            GameEvent(
                id="scope_creep",
                name="需求变更",
                description="客户突然要求增加新功能",
                event_type="negative",
                impact={},  # 特殊处理：工期增加
                probability=0.08,
            ),
            GameEvent(
                id="bug_explosion",
                name="Bug 爆发",
                description="项目出现大量 Bug，需要返工",
                event_type="negative",
                impact={"cash": -2000},
                probability=0.05,
            ),
            GameEvent(
                id="agent_sick",
                name="Agent 生病",
                description="某个 Agent 生病请假",
                event_type="negative",
                impact={},  # 特殊处理：Agent 状态改变
                probability=0.03,
            ),
            GameEvent(
                id="server_crash",
                name="服务器宕机",
                description="开发服务器宕机，进度损失",
                event_type="negative",
                impact={"cash": -1000},
                probability=0.02,
            ),
            GameEvent(
                id="bad_review",
                name="客户差评",
                description="客户对项目不满意，给了差评",
                event_type="negative",
                impact={"reputation": -0.2},
                probability=0.02,
            ),
        ]
        
        return self._weighted_random_choice(events)
    
    def _weighted_random_choice(self, events: List[GameEvent]) -> Optional[GameEvent]:
        """加权随机选择"""
        if not events:
            return None
        
        total_weight = sum(e.probability for e in events)
        if total_weight == 0:
            return None
        
        roll = random.random() * total_weight
        cumulative = 0
        
        for event in events:
            cumulative += event.probability
            if roll <= cumulative:
                return event
        
        return events[-1] if events else None
    
    def get_event_history(self, limit: int = 10) -> List[dict]:
        """获取事件历史"""
        return [e.to_dict() for e in self.event_history[-limit:]]


# 预定义事件池
EVENT_POOL: Dict[str, GameEvent] = {}


def register_event(event: GameEvent) -> None:
    """注册事件到事件池"""
    EVENT_POOL[event.id] = event


def get_event(event_id: str) -> Optional[GameEvent]:
    """从事件池获取事件"""
    return EVENT_POOL.get(event_id)


# 注册默认事件
def init_default_events():
    """初始化默认事件"""
    # 正面事件
    register_event(GameEvent(
        id="bonus_project",
        name="额外项目",
        description="获得一个额外的优质项目",
        event_type="positive",
        impact={"cash": 15000},
    ))
    
    # 负面事件
    register_event(GameEvent(
        id="competitor_poach",
        name="竞争对手挖角",
        description="竞争对手试图挖走你的 Agent",
        event_type="negative",
        impact={"reputation": -0.1},
    ))


# 初始化
init_default_events()
