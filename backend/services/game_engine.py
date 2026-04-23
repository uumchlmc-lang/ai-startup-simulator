"""
游戏引擎核心
管理游戏状态、循环和逻辑
"""

import random
from datetime import datetime
from typing import List, Dict, Optional

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Company, Agent, Project, create_agent, create_project
from services.event_system import EventSystem
from services.save_system import SaveSystem


class GameEngine:
    """游戏引擎类"""
    
    def __init__(self):
        self.company: Optional[Company] = None
        self.event_system = EventSystem()
        self.save_system = SaveSystem()
        self.game_over = False
        self.game_over_reason = None
    
    def new_game(self, company_name: str = "AI 创业公司") -> Company:
        """开始新游戏"""
        self.company = Company(name=company_name)
        self.game_over = False
        self.game_over_reason = None
        
        # 初始赠送 2 个初级 Agent
        self.company.hire_agent("初级程序员", "小王")
        self.company.hire_agent("初级程序员", "小李")
        
        # 初始赠送 1 个项目
        project = create_project("网站开发")
        self.company.projects.append(project)
        
        return self.company
    
    def load_game(self, save_name: str = "autosave") -> Optional[Company]:
        """加载游戏"""
        company = self.save_system.load(save_name)
        if company:
            self.company = company
            self.game_over = False
            self.game_over_reason = None
        return self.company
    
    def save_game(self, save_name: str = "autosave") -> bool:
        """保存游戏"""
        if not self.company:
            return False
        return self.save_system.save(self.company, save_name)
    
    def get_company_status(self) -> dict:
        """获取公司状态"""
        if not self.company:
            return {"error": "No active game"}
        return self.company.get_status()
    
    def next_day(self) -> dict:
        """进入下一天"""
        if not self.company or self.game_over:
            return {"error": "Game not active or game over"}
        
        # 处理下一天
        result = self.company.next_day()
        
        # 触发随机事件
        event = self.event_system.trigger_random_event()
        if event:
            event.apply(self.company)
            result["event"] = event.to_dict()
        
        # 生成新项目 (概率)
        if random.random() < 0.7:  # 70% 概率生成新项目
            new_project = create_project(random.choice(list(create_project.__globals__["PROJECT_TYPES"].keys())))
            self.company.projects.append(new_project)
            result["new_project"] = new_project.to_dict()
        
        # 检查游戏结束
        is_over, reason = self.company.check_game_over()
        if is_over:
            self.game_over = True
            self.game_over_reason = reason
            result["game_over"] = True
            result["game_over_reason"] = reason
        
        # 自动保存
        self.save_game("autosave")
        
        return result
    
    # ========== Agent 管理 ==========
    
    def hire_agent(self, role: str, name: Optional[str] = None) -> dict:
        """雇佣 Agent"""
        if not self.company:
            return {"error": "No active game"}
        
        if len(self.company.agents) >= self.company.get_max_agents():
            return {"error": "Office capacity reached"}
        
        agent = self.company.hire_agent(role, name)
        return {"success": True, "agent": agent.to_dict()}
    
    def fire_agent(self, agent_id: str) -> dict:
        """解雇 Agent"""
        if not self.company:
            return {"error": "No active game"}
        
        success = self.company.fire_agent(agent_id)
        return {"success": success}
    
    def list_agents(self) -> List[dict]:
        """列出所有 Agent"""
        if not self.company:
            return []
        return [a.to_dict() for a in self.company.agents]
    
    def train_agent(self, agent_id: str, training_type: str = "online") -> dict:
        """培训 Agent (Phase 3.2 增强)"""
        if not self.company:
            return {"error": "No active game"}
        
        agent = next((a for a in self.company.agents if a.id == agent_id), None)
        if not agent:
            return {"error": "Agent not found"}
        
        # 培训成本配置
        TRAINING_COSTS = {
            "online": 500,
            "workshop": 1500,
            "external": 3000,
            "conference": 5000,
            "mentor": 8000,
        }
        
        cost = TRAINING_COSTS.get(training_type, 500)
        if self.company.cash < cost:
            return {"error": f"Not enough cash (need ${cost})"}
        
        self.company.cash -= cost
        result = agent.train(training_type, self.company.office_level)
        
        return {
            "success": True,
            "result": result,
            "agent": agent.to_dict(),
        }
    
    # ========== 项目管理 ==========
    
    def list_projects(self, status: Optional[str] = None) -> List[dict]:
        """列出项目"""
        if not self.company:
            return []
        
        projects = self.company.projects
        if status:
            projects = [p for p in projects if p.status == status]
        
        return [p.to_dict() for p in projects]
    
    def accept_project(self, project_id: str) -> dict:
        """接受项目"""
        if not self.company:
            return {"error": "No active game"}
        
        project = next((p for p in self.company.projects if p.id == project_id), None)
        if not project:
            return {"error": "Project not found"}
        
        success = self.company.accept_project(project)
        return {"success": success, "project": project.to_dict()}
    
    def assign_agent(self, agent_id: str, project_id: str) -> dict:
        """分配 Agent 到项目"""
        if not self.company:
            return {"error": "No active game"}
        
        success = self.company.assign_agent_to_project(agent_id, project_id)
        return {"success": success}
    
    def complete_project(self, project_id: str) -> dict:
        """完成项目"""
        if not self.company:
            return {"error": "No active game"}
        
        reward = self.company.complete_project(project_id)
        return {
            "success": reward > 0,
            "reward": reward,
            "project_id": project_id,
        }
    
    # ========== 公司管理 ==========
    
    def rename_company(self, new_name: str) -> dict:
        """改名"""
        if not self.company:
            return {"error": "No active game"}
        
        self.company.name = new_name
        return {"success": True, "name": new_name}
    
    def upgrade_office(self) -> dict:
        """升级办公室"""
        if not self.company:
            return {"error": "No active game"}
        
        success = self.company.upgrade_office()
        return {
            "success": success,
            "office_level": self.company.office_level if success else self.company.office_level,
        }
    
    def research_technology(self, tech_name: str) -> dict:
        """研发科技"""
        if not self.company:
            return {"error": "No active game"}
        
        success = self.company.research_technology(tech_name)
        return {
            "success": success,
            "technologies": self.company.technologies,
        }
    
    # ========== 游戏控制 ==========
    
    def get_available_actions(self) -> List[str]:
        """获取可用操作"""
        if not self.company or self.game_over:
            return []
        
        actions = [
            "next_day",
            "hire_agent",
            "accept_project",
            "assign_agent",
            "complete_project",
            "upgrade_office",
            "research_technology",
            "save_game",
        ]
        
        return actions
    
    def get_game_over_info(self) -> dict:
        """获取游戏结束信息"""
        return {
            "game_over": self.game_over,
            "reason": self.game_over_reason,
            "final_stats": self.company.get_status() if self.company else None,
        }


# 全局游戏实例
_current_game: Optional[GameEngine] = None


def get_current_game() -> GameEngine:
    """获取当前游戏实例"""
    global _current_game
    if _current_game is None:
        _current_game = GameEngine()
    return _current_game


def reset_game() -> GameEngine:
    """重置游戏"""
    global _current_game
    _current_game = GameEngine()
    return _current_game
