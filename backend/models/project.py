"""
Project 数据模型
客户项目的核心属性和行为
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Project:
    """项目类"""
    
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "未命名项目"
    type: str = "网站开发"
    description: str = ""
    
    # 难度 (1-5 星)
    difficulty: int = 1
    
    # 时间和报酬
    deadline_days: int = 7       # 截止日期 (天)
    days_remaining: int = 7      # 剩余天数
    reward: float = 10000.0      # 报酬
    
    # 进度和质量
    progress: int = 0            # 进度 (0-100)
    quality: int = 0             # 质量 (0-100)
    
    # 状态
    status: str = "available"  # available, in_progress, completed, failed, cancelled
    
    # 分配的 Agent
    assigned_agents: List[str] = field(default_factory=list)  # Agent ID 列表
    
    # 客户信息
    client_name: str = "未知客户"
    client_satisfaction: int = 0  # 客户满意度 (0-100)
    
    # 时间记录
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "difficulty": self.difficulty,
            "deadline_days": self.deadline_days,
            "days_remaining": self.days_remaining,
            "reward": self.reward,
            "progress": self.progress,
            "quality": self.quality,
            "status": self.status,
            "assigned_agents": self.assigned_agents,
            "client_name": self.client_name,
            "client_satisfaction": self.client_satisfaction,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        """从字典创建"""
        project = cls()
        project.id = data.get("id", project.id)
        project.name = data.get("name", project.name)
        project.type = data.get("type", project.type)
        project.description = data.get("description", project.description)
        project.difficulty = data.get("difficulty", project.difficulty)
        project.deadline_days = data.get("deadline_days", project.deadline_days)
        project.days_remaining = data.get("days_remaining", project.days_remaining)
        project.reward = data.get("reward", project.reward)
        project.progress = data.get("progress", project.progress)
        project.quality = data.get("quality", project.quality)
        project.status = data.get("status", project.status)
        project.assigned_agents = data.get("assigned_agents", [])
        project.client_name = data.get("client_name", project.client_name)
        project.client_satisfaction = data.get("client_satisfaction", project.client_satisfaction)
        project.created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        project.started_at = datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None
        project.completed_at = datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None
        return project
    
    def start(self) -> bool:
        """开始项目"""
        if self.status != "available":
            return False
        
        self.status = "in_progress"
        self.started_at = datetime.now()
        return True
    
    def add_agent(self, agent_id: str) -> bool:
        """分配 Agent 到项目"""
        if agent_id not in self.assigned_agents:
            self.assigned_agents.append(agent_id)
            return True
        return False
    
    def remove_agent(self, agent_id: str) -> bool:
        """从项目移除 Agent"""
        if agent_id in self.assigned_agents:
            self.assigned_agents.remove(agent_id)
            return True
        return False
    
    def update_progress(self, daily_progress: int) -> None:
        """更新项目进度"""
        self.progress = min(100, self.progress + daily_progress)
        self.days_remaining = max(0, self.days_remaining - 1)
        
        # 检查是否完成
        if self.progress >= 100:
            self.complete()
        # 检查是否超时
        elif self.days_remaining <= 0:
            self.fail()
    
    def calculate_quality(self, agents: list) -> int:
        """
        计算项目质量
        """
        if not agents:
            return 0
        
        # 平均创造力和稳定性
        avg_creativity = sum(a.creativity for a in agents) / len(agents)
        avg_stability = sum(a.stability for a in agents) / len(agents)
        
        # 难度惩罚
        difficulty_penalty = 1.0 - (self.difficulty - 1) * 0.1
        
        # 时间压力
        time_factor = self.days_remaining / max(self.deadline_days, 1)
        
        # 质量分数
        quality = (avg_creativity * 0.6 + avg_stability * 0.4) * difficulty_penalty * time_factor
        
        return min(100, int(quality))
    
    def complete(self) -> float:
        """
        完成项目
        返回实际获得的报酬 (可能有奖金/罚款)
        """
        self.status = "completed"
        self.completed_at = datetime.now()
        
        # 基础报酬
        final_reward = self.reward
        
        # 质量奖金/罚款
        if self.quality >= 90:
            final_reward *= 1.2  # +20% 奖金
        elif self.quality >= 70:
            final_reward *= 1.0  # 正常
        elif self.quality >= 50:
            final_reward *= 0.8  # -20% 罚款
        else:
            final_reward *= 0.5  # -50% 严重罚款
        
        return final_reward
    
    def fail(self) -> None:
        """项目失败"""
        self.status = "failed"
        self.completed_at = datetime.now()
    
    def cancel(self) -> None:
        """取消项目"""
        self.status = "cancelled"


# 项目类型配置
PROJECT_TYPES = {
    "网站开发": {
        "difficulty": 1,
        "deadline_range": (3, 7),
        "reward_range": (5000, 20000),
    },
    "移动 App": {
        "difficulty": 3,
        "deadline_range": (14, 30),
        "reward_range": (20000, 50000),
    },
    "AI 系统集成": {
        "difficulty": 4,
        "deadline_range": (7, 14),
        "reward_range": (10000, 30000),
    },
    "企业软件": {
        "difficulty": 5,
        "deadline_range": (30, 90),
        "reward_range": (50000, 200000),
    },
    "小游戏": {
        "difficulty": 2,
        "deadline_range": (7, 14),
        "reward_range": (8000, 25000),
    },
    "数据分析": {
        "difficulty": 2,
        "deadline_range": (5, 10),
        "reward_range": (6000, 15000),
    },
}


def create_project(project_type: str = "网站开发") -> Project:
    """创建随机项目"""
    import random
    
    config = PROJECT_TYPES.get(project_type, PROJECT_TYPES["网站开发"])
    
    deadline = random.randint(*config["deadline_range"])
    reward = random.randint(*config["reward_range"])
    
    project = Project(
        name=f"{project_type} #{str(uuid.uuid4())[:4]}",
        type=project_type,
        difficulty=config["difficulty"],
        deadline_days=deadline,
        days_remaining=deadline,
        reward=reward,
    )
    
    return project
