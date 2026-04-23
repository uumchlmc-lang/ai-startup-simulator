"""
Agent 数据模型
AI 员工的核心属性和行为
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Agent:
    """Agent 员工类"""
    
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "未命名 Agent"
    role: str = "初级程序员"
    
    # 属性 (0-100)
    efficiency: int = 50      # 工作效率
    creativity: int = 50      # 创造力
    stability: int = 80       # 稳定性
    satisfaction: int = 70    # 满意度
    collaboration: int = 50   # 协作能力 (Phase 3.2 新增)
    
    # 等级 (1-5)
    level: int = 1
    
    # 技能点 (Phase 3.2 新增)
    skill_points: int = 0
    
    # 羁绊天数 (Phase 3.2 新增)
    bond_days: int = 0
    
    # 薪资 (每天)
    salary: int = 1000
    
    # 状态
    status: str = "idle"  # idle, working, resting, sick, resigned
    current_project: Optional[str] = None  # 当前项目 ID
    
    # 时间记录
    hired_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    # 统计数据
    projects_completed: int = 0
    total_earnings: float = 0.0
    training_days: int = 0  # 培训天数 (Phase 3.2 新增)
    
    def to_dict(self) -> dict:
        """转换为字典 (Phase 3.2 增强)"""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "level": self.level,
            "efficiency": self.efficiency,
            "creativity": self.creativity,
            "stability": self.stability,
            "satisfaction": self.satisfaction,
            "collaboration": self.collaboration,  # Phase 3.2 新增
            "skill_points": self.skill_points,  # Phase 3.2 新增
            "bond_days": self.bond_days,  # Phase 3.2 新增
            "training_days": self.training_days,  # Phase 3.2 新增
            "salary": self.salary,
            "status": self.status,
            "current_project": self.current_project,
            "hired_at": self.hired_at.isoformat(),
            "projects_completed": self.projects_completed,
            "total_earnings": self.total_earnings,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Agent":
        """从字典创建 (Phase 3.2 增强)"""
        agent = cls()
        agent.id = data.get("id", agent.id)
        agent.name = data.get("name", agent.name)
        agent.role = data.get("role", agent.role)
        agent.level = data.get("level", agent.level)
        agent.efficiency = data.get("efficiency", agent.efficiency)
        agent.creativity = data.get("creativity", agent.creativity)
        agent.stability = data.get("stability", agent.stability)
        agent.satisfaction = data.get("satisfaction", agent.satisfaction)
        agent.collaboration = data.get("collaboration", 50)  # Phase 3.2 新增
        agent.skill_points = data.get("skill_points", 0)  # Phase 3.2 新增
        agent.bond_days = data.get("bond_days", 0)  # Phase 3.2 新增
        agent.training_days = data.get("training_days", 0)  # Phase 3.2 新增
        agent.salary = data.get("salary", agent.salary)
        agent.status = data.get("status", agent.status)
        agent.current_project = data.get("current_project")
        agent.hired_at = datetime.fromisoformat(data["hired_at"]) if "hired_at" in data else datetime.now()
        agent.projects_completed = data.get("projects_completed", 0)
        agent.total_earnings = data.get("total_earnings", 0.0)
        return agent
    
    def work(self, hours: int = 8) -> int:
        """
        工作，返回贡献的进度点
        """
        if self.status != "idle" and self.status != "working":
            return 0
        
        # 基础效率
        base_progress = self.efficiency * (hours / 8)
        
        # 等级加成
        level_bonus = 1.0 + (self.level - 1) * 0.2
        
        # 满意度影响
        satisfaction_factor = 0.5 + (self.satisfaction / 100) * 0.5
        
        progress = int(base_progress * level_bonus * satisfaction_factor)
        
        # 满意度轻微下降
        self.satisfaction = max(0, self.satisfaction - 1)
        
        return progress
    
    def rest(self) -> None:
        """休息，恢复满意度"""
        self.satisfaction = min(100, self.satisfaction + 10)
        self.status = "idle"
        self.current_project = None
    
    def train(self, training_type: str = "online", office_level: int = 1) -> dict:
        """
        培训，提升属性 (Phase 3.2 增强)
        返回培训结果
        """
        import random
        
        # 培训类型配置
        TRAINING_TYPES = {
            "online": {"days": 1, "cost": 500, "points": 2},
            "workshop": {"days": 3, "cost": 1500, "points": 5},
            "external": {"days": 5, "cost": 3000, "points": 10},
            "conference": {"days": 7, "cost": 5000, "points": 15},
            "mentor": {"days": 10, "cost": 8000, "points": 20},
        }
        
        config = TRAINING_TYPES.get(training_type, TRAINING_TYPES["online"])
        
        # 办公室等级加成
        office_bonus = 1.0 + (office_level - 1) * 0.05
        
        # 创意加成
        creativity_bonus = 1.0 + self.creativity / 100
        
        # 计算实际技能点
        actual_points = int(config["points"] * office_bonus * creativity_bonus)
        
        # 更新属性
        self.skill_points += actual_points
        self.training_days += config["days"]
        self.efficiency = min(100, self.efficiency + random.randint(1, actual_points))
        self.creativity = min(100, self.creativity + random.randint(1, actual_points))
        self.stability = min(100, self.stability + random.randint(1, actual_points))
        self.collaboration = min(100, self.collaboration + random.randint(1, actual_points // 2))
        
        # 检查是否升级
        old_level = self.level
        self.level = min(5, 1 + self.skill_points // 100)
        
        # 升级加薪
        if self.level > old_level:
            self.salary = int(self.salary * 1.3)
        
        return {
            "success": True,
            "training_type": training_type,
            "days": config["days"],
            "cost": config["cost"],
            "skill_points_gained": actual_points,
            "total_skill_points": self.skill_points,
            "leveled_up": self.level > old_level,
            "new_level": self.level,
        }
        
        return False
    
    def check_resignation(self) -> bool:
        """
        检查是否离职
        返回是否离职
        """
        import random
        
        # 满意度低时离职概率高
        if self.satisfaction < 30:
            if random.random() < 0.1:  # 10% 概率
                self.status = "resigned"
                return True
        
        return False


# Agent 角色配置
AGENT_ROLES = {
    # 技术线
    "初级程序员": {"efficiency": 40, "creativity": 40, "stability": 70, "salary": 1000},
    "中级程序员": {"efficiency": 60, "creativity": 60, "stability": 75, "salary": 2000},
    "高级程序员": {"efficiency": 80, "creativity": 75, "stability": 80, "salary": 4000},
    "专家程序员": {"efficiency": 95, "creativity": 90, "stability": 85, "salary": 8000},
    "架构师": {"efficiency": 90, "creativity": 95, "stability": 90, "salary": 12000},
    # 设计线
    "设计师": {"efficiency": 60, "creativity": 85, "stability": 70, "salary": 2500},
    "高级设计师": {"efficiency": 75, "creativity": 95, "stability": 75, "salary": 5000},
    "UI/UX 专家": {"efficiency": 80, "creativity": 98, "stability": 80, "salary": 9000},
    # 产品线
    "产品经理": {"efficiency": 70, "creativity": 80, "stability": 75, "salary": 3500},
    "高级产品经理": {"efficiency": 85, "creativity": 90, "stability": 80, "salary": 7000},
    # 测试线
    "测试工程师": {"efficiency": 65, "creativity": 50, "stability": 85, "salary": 2000},
    "测试专家": {"efficiency": 80, "creativity": 60, "stability": 95, "salary": 6000},
    # 运维线
    "运维工程师": {"efficiency": 70, "creativity": 55, "stability": 90, "salary": 3000},
    "DevOps 专家": {"efficiency": 90, "creativity": 70, "stability": 95, "salary": 10000},
    # 数据线
    "数据分析师": {"efficiency": 75, "creativity": 70, "stability": 80, "salary": 4000},
    "AI 工程师": {"efficiency": 85, "creativity": 95, "stability": 75, "salary": 11000},
}


def create_agent(role: str = "初级程序员", name: Optional[str] = None) -> Agent:
    """创建 Agent"""
    config = AGENT_ROLES.get(role, AGENT_ROLES["初级程序员"])
    agent = Agent(
        name=name or f"{role}#{str(uuid.uuid4())[:4]}",
        role=role,
        efficiency=config["efficiency"],
        creativity=config["creativity"],
        stability=config["stability"],
        salary=config["salary"],
    )
    return agent
