"""
Company 数据模型
玩家公司的核心属性和行为
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
import uuid
import json

from .agent import Agent, create_agent
from .project import Project, create_project


@dataclass
class Company:
    """公司类"""
    
    # 基本信息
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "AI 创业公司"
    
    # 财务
    cash: float = 50000.0       # 现金 (初始$50k)
    total_earnings: float = 0.0  # 总收入
    total_expenses: float = 0.0  # 总支出
    
    # 声誉
    reputation: float = 3.0      # 口碑 (0-5)
    
    # 游戏进度
    day: int = 0                 # 游戏天数
    office_level: int = 1        # 办公室等级 (1-5)
    
    # 资源
    agents: List[Agent] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    
    # 统计
    projects_completed: int = 0
    projects_failed: int = 0
    total_days: int = 0
    
    # 羁绊系统 (Phase 3.2 新增)
    bond_days: int = 0  # 羁绊累积天数
    
    # 时间记录
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """转换为字典 (用于存档)"""
        return {
            "id": self.id,
            "name": self.name,
            "cash": self.cash,
            "total_earnings": self.total_earnings,
            "total_expenses": self.total_expenses,
            "reputation": self.reputation,
            "day": self.day,
            "office_level": self.office_level,
            "agents": [a.to_dict() for a in self.agents],
            "projects": [p.to_dict() for p in self.projects],
            "technologies": self.technologies,
            "projects_completed": self.projects_completed,
            "projects_failed": self.projects_failed,
            "total_days": self.total_days,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Company":
        """从字典创建 (用于读档)"""
        company = cls()
        company.id = data.get("id", company.id)
        company.name = data.get("name", company.name)
        company.cash = data.get("cash", company.cash)
        company.total_earnings = data.get("total_earnings", company.total_earnings)
        company.total_expenses = data.get("total_expenses", company.total_expenses)
        company.reputation = data.get("reputation", company.reputation)
        company.day = data.get("day", company.day)
        company.office_level = data.get("office_level", company.office_level)
        company.agents = [Agent.from_dict(a) for a in data.get("agents", [])]
        company.projects = [Project.from_dict(p) for p in data.get("projects", [])]
        company.technologies = data.get("technologies", [])
        company.projects_completed = data.get("projects_completed", 0)
        company.projects_failed = data.get("projects_failed", 0)
        company.total_days = data.get("total_days", 0)
        company.created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else datetime.now()
        company.last_updated = datetime.fromisoformat(data["last_updated"]) if "last_updated" in data else datetime.now()
        return company
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> "Company":
        """从 JSON 字符串创建"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    # ========== Agent 管理 ==========
    
    def hire_agent(self, role: str = "初级程序员", name: Optional[str] = None) -> Agent:
        """雇佣 Agent"""
        agent = create_agent(role, name)
        self.agents.append(agent)
        return agent
    
    def fire_agent(self, agent_id: str) -> bool:
        """解雇 Agent"""
        for i, agent in enumerate(self.agents):
            if agent.id == agent_id:
                self.agents.pop(i)
                return True
        return False
    
    def get_available_agents(self) -> List[Agent]:
        """获取可用的 Agent"""
        return [a for a in self.agents if a.status == "idle"]
    
    def get_agent_daily_salary(self) -> int:
        """计算每日总薪资"""
        return sum(a.salary for a in self.agents)
    
    # ========== 项目管理 ==========
    
    def get_available_projects(self) -> List[Project]:
        """获取可接受的项目"""
        return [p for p in self.projects if p.status == "available"]
    
    def get_active_projects(self) -> List[Project]:
        """获取进行中的项目"""
        return [p for p in self.projects if p.status == "in_progress"]
    
    def accept_project(self, project: Project) -> bool:
        """接受项目"""
        if project.status != "available":
            return False
        project.start()
        
        # 自动分配所有空闲员工到项目
        for agent in self.agents:
            if agent.status == "idle":
                self.assign_agent_to_project(agent.id, project.id)
        
        return True
    
    def assign_agent_to_project(self, agent_id: str, project_id: str) -> bool:
        """分配 Agent 到项目"""
        agent = next((a for a in self.agents if a.id == agent_id), None)
        project = next((p for p in self.projects if p.id == project_id), None)
        
        if not agent or not project:
            return False
        
        if agent.status != "idle":
            return False
        
        agent.status = "working"
        agent.current_project = project_id
        project.add_agent(agent_id)
        
        return True
    
    def complete_project(self, project_id: str) -> float:
        """完成项目，返回实际报酬"""
        project = next((p for p in self.projects if p.id == project_id), None)
        if not project:
            return 0.0
        
        # 计算质量
        agents = [a for a in self.agents if a.id in project.assigned_agents]
        project.quality = project.calculate_quality(agents)
        
        # 完成项目
        reward = project.complete()
        self.cash += reward
        self.total_earnings += reward
        self.projects_completed += 1
        
        # 更新 Agent 统计
        for agent in agents:
            agent.projects_completed += 1
            agent.total_earnings += reward / len(agents)
            agent.rest()  # 完成后休息
        
        # 更新声誉
        if project.quality >= 80:
            self.reputation = min(5.0, self.reputation + 0.1)
        elif project.quality < 50:
            self.reputation = max(0.0, self.reputation - 0.1)
        
        return reward
    
    # ========== 游戏进程 ==========
    
    def next_day(self) -> dict:
        """
        进入下一天
        返回当日结算信息
        """
        self.day += 1
        self.total_days += 1
        
        # 支出
        daily_salary = self.get_agent_daily_salary()
        office_rent = self.get_office_rent()
        daily_expenses = daily_salary + office_rent
        
        self.cash -= daily_expenses
        self.total_expenses += daily_expenses
        
        # 更新进行中的项目
        for project in self.get_active_projects():
            # 计算当日进度
            agents = [a for a in self.agents if a.id in project.assigned_agents]
            daily_progress = sum(a.work() for a in agents)
            
            # 难度惩罚
            difficulty_penalty = 1.0 - (project.difficulty - 1) * 0.1
            daily_progress = int(daily_progress * difficulty_penalty)
            
            project.update_progress(daily_progress)
        
        # Phase 3.2: 更新羁绊天数
        self.bond_days += 1
        for agent in self.agents:
            agent.bond_days = self.bond_days
        
        # 检查 Agent 离职
        resigned = []
        for agent in self.agents:
            if agent.check_resignation():
                resigned.append(agent.name)
        
        # 清理离职 Agent
        self.agents = [a for a in self.agents if a.status != "resigned"]
        
        # 检查破产
        game_over = self.cash < -50000
        game_over_reason = None
        if game_over:
            game_over_reason = "bankruptcy"
        elif self.reputation <= 0:
            game_over = True
            game_over_reason = "reputation"
        
        self.last_updated = datetime.now()
        
        return {
            "day": self.day,
            "income": 0,
            "expenses": daily_expenses,
            "salary": daily_salary,
            "rent": office_rent,
            "projects_completed": [p.name for p in self.projects if p.status == "completed" and p.completed_at and p.completed_at.date() == datetime.now().date()],
            "resigned_agents": resigned,
            "game_over": game_over,
            "game_over_reason": game_over_reason,
        }
    
    def get_office_rent(self) -> int:
        """获取办公室租金"""
        office_rents = {
            1: 0,      # 车库 - 免费
            2: 5000,   # 共享办公
            3: 15000,  # 独立办公室
            4: 30000,  # 科技园区
            5: 50000,  # AI 总部
        }
        return office_rents.get(self.office_level, 0)
    
    def upgrade_office(self) -> bool:
        """升级办公室"""
        if self.office_level >= 5:
            return False
        
        upgrade_costs = {
            1: 10000,   # 车库 → 共享办公
            2: 30000,   # 共享办公 → 独立办公室
            3: 60000,   # 独立办公室 → 科技园区
            4: 100000,  # 科技园区 → AI 总部
        }
        
        cost = upgrade_costs.get(self.office_level, 0)
        if self.cash >= cost:
            self.cash -= cost
            self.office_level += 1
            return True
        
        return False
    
    def get_max_agents(self) -> int:
        """获取办公室最大 Agent 容量"""
        office_capacities = {
            1: 5,   # 车库
            2: 15,  # 共享办公
            3: 30,  # 独立办公室
            4: 50,  # 科技园区
            5: 100, # AI 总部
        }
        return office_capacities.get(self.office_level, 5)
    
    # ========== 科技研发 ==========
    
    def research_technology(self, tech_name: str) -> bool:
        """研发科技"""
        if tech_name in self.technologies:
            return False  # 已拥有
        
        tech_costs = {
            "代码生成器": 50000,
            "自动测试": 30000,
            "项目管理 AI": 40000,
            "远程协作": 20000,
            "云服务优化": 25000,
        }
        
        cost = tech_costs.get(tech_name, 0)
        if self.cash >= cost:
            self.cash -= cost
            self.technologies.append(tech_name)
            return True
        
        return False
    
    def has_technology(self, tech_name: str) -> bool:
        """检查是否拥有科技"""
        return tech_name in self.technologies
    
    # ========== 游戏状态 ==========
    
    def get_status(self) -> dict:
        """获取公司状态"""
        return {
            "name": self.name,
            "day": self.day,
            "cash": self.cash,
            "reputation": self.reputation,
            "office_level": self.office_level,
            "agent_count": len(self.agents),
            "max_agents": self.get_max_agents(),
            "active_projects": len(self.get_active_projects()),
            "technologies": len(self.technologies),
            "daily_expenses": self.get_agent_daily_salary() + self.get_office_rent(),
        }
    
    def check_game_over(self) -> tuple:
        """
        检查游戏是否结束
        返回 (is_over, reason)
        """
        if self.cash < -50000:
            return True, "bankruptcy"
        if self.reputation <= 0:
            return True, "reputation"
        return False, None
