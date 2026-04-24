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
    cash: float = 75000.0       # 现金 (初始$75k)
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
    
    # 羁绊等级配置
    BOND_TIERS = {
        0: {"name": "陌生", "quality_bonus": 0.0, "min_days": 0},
        1: {"name": "相识", "quality_bonus": 0.05, "min_days": 8},
        2: {"name": "默契", "quality_bonus": 0.10, "min_days": 31},
        3: {"name": "信赖", "quality_bonus": 0.15, "min_days": 61},
        4: {"name": "灵魂伴侣", "quality_bonus": 0.20, "min_days": 100},
    }
    
    # Phase 3.3: 设备系统
    equipments: List[str] = field(default_factory=list)
    
    # Phase 3.3: 品牌系统
    brand_level: float = 0.0
    last_brand_check_day: int = 0
    brand_warning_until: int = 0
    brand_maintenance_due: bool = False
    
    # Phase 3.3: 融资系统
    equity_sold: float = 0.0
    investors: List[dict] = field(default_factory=list)
    dividend_accumulator: float = 0.0
    last_dividend_day: int = 0
    
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
            "bond_days": self.bond_days,
            "equipments": self.equipments,
            "brand_level": self.brand_level,
            "last_brand_check_day": self.last_brand_check_day,
            "brand_warning_until": self.brand_warning_until,
            "brand_maintenance_due": self.brand_maintenance_due,
            "equity_sold": self.equity_sold,
            "investors": self.investors,
            "dividend_accumulator": self.dividend_accumulator,
            "last_dividend_day": self.last_dividend_day,
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
        company.bond_days = data.get("bond_days", 0)
        company.equipments = data.get("equipments", [])
        company.brand_level = data.get("brand_level", 0.0)
        company.last_brand_check_day = data.get("last_brand_check_day", 0)
        company.brand_warning_until = data.get("brand_warning_until", 0)
        company.brand_maintenance_due = data.get("brand_maintenance_due", False)
        company.equity_sold = data.get("equity_sold", 0.0)
        company.investors = data.get("investors", [])
        company.dividend_accumulator = data.get("dividend_accumulator", 0.0)
        company.last_dividend_day = data.get("last_dividend_day", 0)
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
        
        # 如果项目不在公司项目列表中，添加它
        if project not in self.projects:
            self.projects.append(project)
        
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
    
    # ========== Phase 3.3: 设备系统 ==========
    
    EQUIPMENT_CONFIG = {
        "高速网络": {"cost": 10000, "office_required": 1, "bonus": 0.05},
        "开发者工作站": {"cost": 25000, "office_required": 2, "bonus": 0.10, "programmer_bonus": 0.10},
        "云服务器集群": {"cost": 50000, "office_required": 3, "bonus": 0.10},
        "测试实验室": {"cost": 35000, "office_required": 3, "bonus": 0.05},
        "AI 训练集群": {"cost": 150000, "office_required": 4, "bonus": 0.20},
    }
    
    def buy_equipment(self, equipment_name: str) -> dict:
        """购买设备"""
        config = self.EQUIPMENT_CONFIG.get(equipment_name)
        if not config:
            return {"success": False, "error": f"未知设备: {equipment_name}"}
        
        if equipment_name in self.equipments:
            return {"success": False, "error": "已购买该设备"}
        
        if self.office_level < config["office_required"]:
            return {"success": False, "error": f"办公室等级不足 (需要 Lv.{config['office_required']})"}
        
        if self.cash < config["cost"]:
            return {"success": False, "error": "现金不足"}
        
        self.cash -= config["cost"]
        self.equipments.append(equipment_name)
        return {"success": True, "equipment": equipment_name}
    
    def get_equipment_bonus(self) -> float:
        """获取设备总加成 (用于项目报酬倍率)"""
        bonus = 0.0
        for eq in self.equipments:
            config = self.EQUIPMENT_CONFIG.get(eq, {})
            bonus += config.get("bonus", 0.0)
        return bonus
    
    def get_programmer_bonus(self) -> float:
        """获取程序员效率加成"""
        bonus = 0.0
        for eq in self.equipments:
            config = self.EQUIPMENT_CONFIG.get(eq, {})
            bonus += config.get("programmer_bonus", 0.0)
        return bonus
    
    # ========== Phase 3.3: 品牌系统 ==========
    
    BRAND_CONFIG = {
        0: {"name": "无名小卒", "daily_cost": 0, "reward_mult": 1.0, "good_project_bonus": 0.0},
        1: {"name": "地方知名", "daily_cost": 500, "reward_mult": 1.1, "good_project_bonus": 0.10},
        2: {"name": "行业新锐", "daily_cost": 1000, "reward_mult": 1.2, "good_project_bonus": 0.10},
        3: {"name": "知名公司", "daily_cost": 2000, "reward_mult": 1.3, "good_project_bonus": 0.20},
        4: {"name": "行业巨头", "daily_cost": 3500, "reward_mult": 1.5, "good_project_bonus": 0.30},
        5: {"name": "科技帝国", "daily_cost": 5000, "reward_mult": 2.0, "good_project_bonus": 0.50},
    }
    
    MARKETING_CONFIG = {
        "社交媒体推广": {"cost": 15000, "level_up": 0.5},
        "行业展会参展": {"cost": 30000, "level_up": 1.0},
        "电视广告": {"cost": 80000, "level_up": 1.5},
        "全球发布会": {"cost": 200000, "level_up": 2.0},
    }
    
    def get_brand_multiplier(self) -> float:
        """获取品牌倍率"""
        level = self.brand_level
        if level >= 5: return 2.0
        if level >= 4: return 1.5
        if level >= 3: return 1.3
        if level >= 2: return 1.2
        if level >= 1: return 1.1
        if level >= 0.5: return 1.05
        return 1.0
    
    def get_brand_daily_cost(self) -> float:
        """获取品牌日维护费"""
        level = int(self.brand_level)
        return self.BRAND_CONFIG.get(level, self.BRAND_CONFIG[0])["daily_cost"]
    
    def run_marketing(self, campaign_name: str) -> dict:
        """执行营销活动"""
        config = self.MARKETING_CONFIG.get(campaign_name)
        if not config:
            return {"success": False, "error": f"未知营销活动: {campaign_name}"}
        
        if self.cash < config["cost"]:
            return {"success": False, "error": "现金不足"}
        
        if self.brand_level >= 5:
            return {"success": False, "error": "品牌已达最高等级"}
        
        self.cash -= config["cost"]
        self.brand_level = min(5.0, self.brand_level + config["level_up"])
        return {"success": True, "brand_level": self.brand_level}
    
    def maintain_brand(self, days: int = 30) -> dict:
        """品牌维护续费"""
        daily_cost = self.get_brand_daily_cost()
        total_cost = daily_cost * days
        
        if daily_cost == 0:
            return {"success": True, "message": "品牌等级 0，无需维护"}
        
        if self.cash < total_cost:
            return {"success": False, "error": "现金不足"}
        
        self.cash -= total_cost
        self.total_expenses += total_cost
        self.brand_maintenance_due = False
        return {"success": True, "cost": total_cost}
    
    def get_total_project_multiplier(self) -> float:
        """品牌倍率 + 设备加成，加算，上限 2.5x"""
        brand_base = self.get_brand_multiplier()
        equipment_bonus = self.get_equipment_bonus()
        return min(brand_base + equipment_bonus, 2.5)
    
    # ========== Phase 3.3: 融资系统 ==========
    
    FUNDING_CONFIG = {
        "种子轮": {"amount": 100000, "equity": 0.10, "min_day": 10, "min_reputation": 0, "dividend_rate": 0.05},
        "天使轮": {"amount": 300000, "equity": 0.15, "min_day": 30, "min_reputation": 3.5, "dividend_rate": 0.08},
        "A 轮": {"amount": 800000, "equity": 0.20, "min_day": 60, "min_reputation": 4.0, "dividend_rate": 0.10},
        "B 轮": {"amount": 2000000, "equity": 0.15, "min_day": 100, "min_reputation": 4.5, "dividend_rate": 0.12},
        "IPO": {"amount": 5000000, "equity": 0.10, "min_day": 150, "min_reputation": 4.8, "dividend_rate": 0.15},
    }
    
    def apply_funding(self, round_name: str) -> dict:
        """申请融资"""
        config = self.FUNDING_CONFIG.get(round_name)
        if not config:
            return {"success": False, "error": f"未知融资轮次: {round_name}"}
        
        if self.day < config["min_day"]:
            return {"success": False, "error": f"需要第 {config['min_day']} 天以后"}
        
        if self.reputation < config["min_reputation"]:
            return {"success": False, "error": f"需要 reputation ≥ {config['min_reputation']}"}
        
        # 检查是否已融资过该轮次
        for inv in self.investors:
            if inv.get("round") == round_name:
                return {"success": False, "error": f"{round_name}已融资"}
        
        self.cash += config["amount"]
        self.equity_sold += config["equity"]
        self.investors.append({
            "round": round_name,
            "equity": config["equity"],
            "dividend_rate": config["dividend_rate"],
            "day": self.day,
        })
        
        return {
            "success": True,
            "cash": self.cash,
            "equity_sold": self.equity_sold,
            "round": round_name,
        }
    
    def get_total_dividend_rate(self) -> float:
        """获取总分红比例"""
        return sum(inv.get("dividend_rate", 0) for inv in self.investors)
    
    def buyback_equity(self, amount: float) -> dict:
        """回购股权"""
        if self.total_earnings <= 0:
            return {"success": False, "error": "公司无盈利，无法回购"}
        
        net_profit = max(self.total_earnings - self.total_expenses, 1)
        valuation = net_profit * (1 + self.reputation * 0.2)
        
        if valuation <= 1:
            return {"success": False, "error": "公司无盈利，无法回购"}
        
        if self.cash < amount:
            return {"success": False, "error": "现金不足"}
        
        if self.equity_sold <= 0:
            return {"success": False, "error": "无股权可回购"}
        
        equity_bought = amount / valuation
        equity_bought = min(equity_bought, self.equity_sold)  # 不能超过已售股权
        
        self.cash -= amount
        self.equity_sold -= equity_bought
        
        return {
            "success": True,
            "equity_bought": equity_bought,
            "equity_sold": self.equity_sold,
            "valuation": valuation,
        }
    
    # ========== 羁绊系统 ==========
    
    def get_bond_tier(self) -> dict:
        """获取当前羁绊等级"""
        tier = 0
        for t in sorted(self.BOND_TIERS.keys(), reverse=True):
            if self.bond_days >= self.BOND_TIERS[t]["min_days"]:
                tier = t
                break
        return {
            "tier": tier,
            "name": self.BOND_TIERS[tier]["name"],
            "quality_bonus": self.BOND_TIERS[tier]["quality_bonus"],
            "bond_days": self.bond_days,
            "next_tier": min(tier + 1, 4) if tier < 4 else None,
            "days_to_next": (
                self.BOND_TIERS[tier + 1]["min_days"] - self.bond_days
                if tier < 4
                else 0
            ),
        }
    
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
        
        # 羁绊加成
        bond_tier = self.get_bond_tier()
        if bond_tier["quality_bonus"] > 0:
            reward *= (1 + bond_tier["quality_bonus"])
        
        # 品牌+设备总加成
        total_mult = self.get_total_project_multiplier()
        if total_mult > 1.0:
            reward *= total_mult
        
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
        equipment_bonus = self.get_equipment_bonus()
        programmer_bonus = self.get_programmer_bonus()
        for project in self.get_active_projects():
            # 计算当日进度
            agents = [a for a in self.agents if a.id in project.assigned_agents]
            daily_progress = 0
            for a in agents:
                base_work = a.work()
                # 开发者工作站加成
                if programmer_bonus > 0 and "程序员" in a.role:
                    base_work = int(base_work * (1 + programmer_bonus))
                daily_progress += base_work
            
            # 难度惩罚
            difficulty_penalty = 1.0 - (project.difficulty - 1) * 0.1
            daily_progress = int(daily_progress * difficulty_penalty)
            
            # 设备加成（进度和报酬统一用 bonus）
            if equipment_bonus > 0:
                daily_progress = int(daily_progress * (1 + equipment_bonus))
            
            project.update_progress(daily_progress)
        
        # Phase 3.2: 更新羁绊天数
        self.bond_days += 1
        for agent in self.agents:
            agent.bond_days = self.bond_days
        
        # Phase 3.3: 品牌维护费 - 每 30 天扣除
        if self.day > 0 and self.day % 30 == 0:
            brand_cost = self.get_brand_daily_cost() * 30
            if brand_cost > 0:
                if self.cash >= brand_cost:
                    self.cash -= brand_cost
                    self.total_expenses += brand_cost
                    self.brand_maintenance_due = False
                else:
                    self.brand_maintenance_due = True
        
        # Phase 3.3: 品牌衰减 - 每 7 天检查
        if self.day > 0 and self.day % 7 == 0:
            daily_cost = self.get_brand_daily_cost()
            # 如果品牌等级 > 0 且现金不足以支付 7 天维护费，标记维护不足
            if daily_cost > 0 and self.cash < daily_cost * 7:
                self.brand_maintenance_due = True
            
            if self.brand_maintenance_due:
                if self.brand_warning_until > 0 and self.day >= self.brand_warning_until:
                    # 宽限期已过，降级
                    self.brand_level = max(0, self.brand_level - 0.5)
                    self.brand_warning_until = 0
                    self.brand_maintenance_due = False
                elif self.brand_warning_until == 0:
                    # 第一次发现，给 3 天宽限期
                    self.brand_warning_until = self.day + 3
        
        # Phase 3.3: 分红计算 - 每 30 天结算
        dividend_rate = self.get_total_dividend_rate()
        if dividend_rate > 0 and self.day > 0 and self.day % 30 == 0:
            # 净利润 = 收入 - 支出
            net_profit = max(self.total_earnings - self.total_expenses, 0)
            # 计算上次分红以来的净利润增量
            dividend = net_profit * dividend_rate
            if self.cash >= dividend:
                self.cash -= dividend
                self.total_expenses += dividend
                self.dividend_accumulator = 0
            else:
                self.dividend_accumulator += dividend
                # 无法支付分红，声誉下降
                self.reputation = max(0, self.reputation - 0.2)
        
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
        
        # Phase 3.3: 创始人出局检查
        if self.equity_sold > 0.5:
            game_over = True
            game_over_reason = "founder_out"
        
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
        bond = self.get_bond_tier()
        brand_name = self.BRAND_CONFIG.get(int(self.brand_level), self.BRAND_CONFIG[0])["name"]
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
            "bond": bond,
            "equipments": self.equipments,
            "brand_level": self.brand_level,
            "brand_name": brand_name,
            "equity_sold": self.equity_sold,
            "investors": self.investors,
            "founder_out": self.equity_sold > 0.5,
            "dividend_rate": self.get_total_dividend_rate(),
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
