"""
成就检查引擎
检查并解锁成就
"""

from typing import List, Dict, Optional
from datetime import datetime


class Achievement:
    """成就定义"""
    
    def __init__(self, id: str, name: str, description: str, icon: str, category: str, condition: callable):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.category = category
        self.condition = condition  # callable(company) -> bool


# ========== 成就定义 ==========

ACHIEVEMENTS = {
    # 成长成就 (10)
    "first_project": Achievement("first_project", "迈出第一步", "完成了第一个项目", "🎯", "成长", 
        lambda c: c.projects_completed >= 1),
    "ten_projects": Achievement("ten_projects", "初出茅庐", "完成了 10 个项目", "🌱", "成长",
        lambda c: c.projects_completed >= 10),
    "fifty_projects": Achievement("fifty_projects", "渐入佳境", "完成了 50 个项目", "🌿", "成长",
        lambda c: c.projects_completed >= 50),
    "hundred_projects": Achievement("hundred_projects", "身经百战", "完成了 100 个项目", "🔥", "成长",
        lambda c: c.projects_completed >= 100),
    "hundred_days": Achievement("hundred_days", "创业老兵", "公司运营超过 100 天", "📅", "成长",
        lambda c: c.day >= 100),
    "three_sixty_five_days": Achievement("three_sixty_five_days", "十年磨剑", "公司运营超过 365 天", "⏳", "成长",
        lambda c: c.day >= 365),
    "garage_legend": Achievement("garage_legend", "车库传奇", "从车库创业到 AI 总部", "🏠", "成长",
        lambda c: c.office_level >= 5),
    "fame_five": Achievement("fame_five", "名声大噪", "口碑达到 5.0", "⭐", "成长",
        lambda c: c.reputation >= 5.0),
    "industry_benchmark": Achievement("industry_benchmark", "行业标杆", "口碑 5.0 且完成 100 个项目", "🏆", "成长",
        lambda c: c.reputation >= 5.0 and c.projects_completed >= 100),
    "seven_thirty_days": Achievement("seven_thirty_days", "百年老店", "公司运营超过 730 天", "🎂", "成长",
        lambda c: c.day >= 730),
    
    # 项目成就 (8)
    "perfect_quality": Achievement("perfect_quality", "完美交付", "单次项目质量达到 100", "💎", "项目",
        lambda c: getattr(c, '_last_project_quality', 0) == 100),
    "speed_demon": Achievement("speed_demon", "速战速决", "在截止日前 50% 时间完成项目", "⚡", "项目",
        lambda c: getattr(c, '_last_project_early', False)),
    "buzzer_beater": Achievement("buzzer_beater", "压哨绝杀", "在截止日前 1 天完成项目", "🚨", "项目",
        lambda c: getattr(c, '_last_project_buzzer', False)),
    "full_stack": Achievement("full_stack", "全栈高手", "完成过所有 13 种项目类型", "🎨", "项目",
        lambda c: len(getattr(c, 'completed_project_types', set())) >= 13),
    "big_deal": Achievement("big_deal", "大单王", "单笔项目报酬超过 $500,000", "💰", "项目",
        lambda c: getattr(c, 'max_single_reward', 0) >= 500000),
    "quality_control": Achievement("quality_control", "质量控", "累计 50 次项目质量 ≥ 90", "🎯", "项目",
        lambda c: getattr(c, 'high_quality_count', 0) >= 50),
    "failed_five": Achievement("failed_five", "烂尾楼", "项目失败次数达到 5", "💀", "项目",
        lambda c: c.projects_failed >= 5),
    "comeback_king": Achievement("comeback_king", "逆风翻盘", "失败后连续完成 10 个项目", "🔄", "项目",
        lambda c: getattr(c, 'consecutive_completions', 0) >= 10),
    
    # 团队成就 (7)
    "first_hire": Achievement("first_hire", "光杆司令", "雇佣了第一个员工", "👤", "团队",
        lambda c: len(c.agents) >= 1),
    "ten_agents": Achievement("ten_agents", "十人团", "团队达到 10 人", "👥", "团队",
        lambda c: len(c.agents) >= 10),
    "hundred_agents": Achievement("hundred_agents", "百人战队", "团队达到 100 人", "🏢", "团队",
        lambda c: len(c.agents) >= 100),
    "mentor": Achievement("mentor", "伯乐", "将一名员工从 Lv1 培养到 Lv10", "🎓", "团队",
        lambda c: any(a.level >= 10 for a in c.agents) and getattr(c, 'had_level_1_agent', False)),
    "master_teachers": Achievement("master_teachers", "名师出高徒", "拥有 5 名 Lv10+ 员工", "🧙", "团队",
        lambda c: sum(1 for a in c.agents if a.level >= 10) >= 5),
    "iron_camp": Achievement("iron_camp", "铁打的营盘", "没有员工离职超过 100 天", "🛡️", "团队",
        lambda c: getattr(c, 'days_without_resignation', 0) >= 100),
    "heartless": Achievement("heartless", "铁石心肠", "解雇了 10 名员工", "😈", "团队",
        lambda c: getattr(c, 'total_fired', 0) >= 10),
    
    # 设备成就 (4)
    "first_equipment": Achievement("first_equipment", "网速飞起", "购买了第一个设备", "🌐", "设备",
        lambda c: len(c.equipments) >= 1),
    "all_equipment": Achievement("all_equipment", "装备齐全", "集齐所有 5 种设备", "🏆", "设备",
        lambda c: len(c.equipments) >= 5),
    "rich_company": Achievement("rich_company", "土豪公司", "设备总投入超过 $200,000", "💰", "设备",
        lambda c: getattr(c, 'equipment_total_spent', 0) >= 200000),
    "geek_paradise": Achievement("geek_paradise", "极客天堂", "购买了 AI 训练集群", "🤖", "设备",
        lambda c: "AI 训练集群" in c.equipments),
    
    # 品牌成就 (5)
    "brand_lv1": Achievement("brand_lv1", "小有名气", "品牌达到 Lv1", "🌒", "品牌",
        lambda c: c.brand_level >= 1),
    "brand_lv2": Achievement("brand_lv2", "行业新锐", "品牌达到 Lv2", "🌓", "品牌",
        lambda c: c.brand_level >= 2),
    "brand_lv3": Achievement("brand_lv3", "行业焦点", "品牌达到 Lv3", "🌔", "品牌",
        lambda c: c.brand_level >= 3),
    "brand_lv4": Achievement("brand_lv4", "行业巨头", "品牌达到 Lv4", "🌕", "品牌",
        lambda c: c.brand_level >= 4),
    "brand_lv5": Achievement("brand_lv5", "科技帝国", "品牌达到 Lv5", "🌟", "品牌",
        lambda c: c.brand_level >= 5),
    
    # 融资成就 (7)
    "seed_round": Achievement("seed_round", "第一桶金", "完成种子轮融资", "🌱", "融资",
        lambda c: any(i.get("round") == "种子轮" for i in c.investors)),
    "angel_round": Achievement("angel_round", "资本宠儿", "完成天使轮融资", "👼", "融资",
        lambda c: any(i.get("round") == "天使轮" for i in c.investors)),
    "series_a": Achievement("series_a", "A 轮玩家", "完成 A 轮融资", "🅰️", "融资",
        lambda c: any(i.get("round") == "A 轮" for i in c.investors)),
    "series_b": Achievement("series_b", "B 轮大佬", "完成 B 轮融资", "🅱️", "融资",
        lambda c: any(i.get("round") == "B 轮" for i in c.investors)),
    "ipo": Achievement("ipo", "上市敲钟", "完成 IPO", "📈", "融资",
        lambda c: any(i.get("round") == "IPO" for i in c.investors)),
    "all_funding": Achievement("all_funding", "融资之王", "完成全部 5 轮融资", "👑", "融资",
        lambda c: len(c.investors) >= 5),
    "equity_sold_fifty": Achievement("equity_sold_fifty", "半壁江山", "出让股权超过 50%", "⚠️", "融资",
        lambda c: c.equity_sold >= 0.5),
    
    # 财务成就 (5)
    "first_earnings": Achievement("first_earnings", "第一桶金", "累计收入达到 $100,000", "💵", "财务",
        lambda c: c.total_earnings >= 100000),
    "million_club": Achievement("million_club", "百万俱乐部", "累计收入达到 $1,000,000", "💎", "财务",
        lambda c: c.total_earnings >= 1000000),
    "ten_million": Achievement("ten_million", "千万富翁", "累计收入达到 $10,000,000", "🏦", "财务",
        lambda c: c.total_earnings >= 10000000),
    "profitable": Achievement("profitable", "盈利模式", "净利润超过 $500,000", "📊", "财务",
        lambda c: (c.total_earnings - c.total_expenses) >= 500000),
    "cash_king": Achievement("cash_king", "现金为王", "现金储备超过 $5,000,000", "🤑", "财务",
        lambda c: c.cash >= 5000000),
    
    # 隐藏成就 (6)
    "speed_demon_2": Achievement("speed_demon_2", "闪电侠", "第 1 天就完成项目", "⚡", "隐藏",
        lambda c: c.day == 1 and c.projects_completed >= 1),
    "broke": Achievement("broke", "破产边缘", "现金低于 -$10,000", "📉", "隐藏",
        lambda c: c.cash <= -10000),
    "reputation_zero": Achievement("reputation_zero", "声名狼藉", "口碑降至 0", "💔", "隐藏",
        lambda c: c.reputation <= 0),
    "solo_athlete": Achievement("solo_athlete", "独行侠", "没有员工的情况下完成 5 个项目", "🏃", "隐藏",
        lambda c: len(c.agents) == 0 and c.projects_completed >= 5),
    "equipment_addict": Achievement("equipment_addict", "设备控", "重复购买同一设备", "🔧", "隐藏",
        lambda c: getattr(c, 'tried_duplicate_equipment', False)),
    "brand_jumper": Achievement("brand_jumper", "品牌跳跃者", "单次营销活动提升 2 级品牌", "🎪", "隐藏",
        lambda c: getattr(c, 'big_brand_jump', False)),
}


class AchievementEngine:
    """成就检查引擎"""
    
    def __init__(self):
        self.achievements = ACHIEVEMENTS
    
    def check_all(self, company) -> List[str]:
        """检查所有成就，返回新解锁的成就 ID 列表"""
        unlocked = set(company.achievements)
        new_unlocks = []
        
        for aid, achievement in self.achievements.items():
            if aid not in unlocked:
                try:
                    if achievement.condition(company):
                        new_unlocks.append(aid)
                        company.achievements.append(aid)
                except Exception:
                    # 某些成就条件可能在特定状态下不可用
                    pass
        
        return new_unlocks
    
    def check_category(self, company, category: str) -> List[str]:
        """检查特定分类的成就"""
        unlocked = set(company.achievements)
        new_unlocks = []
        
        for aid, achievement in self.achievements.items():
            if achievement.category == category and aid not in unlocked:
                try:
                    if achievement.condition(company):
                        new_unlocks.append(aid)
                        company.achievements.append(aid)
                except Exception:
                    pass
        
        return new_unlocks
    
    def get_achievement(self, achievement_id: str) -> Optional[dict]:
        """获取成就信息"""
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return None
        return {
            "id": achievement.id,
            "name": achievement.name,
            "description": achievement.description,
            "icon": achievement.icon,
            "category": achievement.category,
        }
    
    def get_all_achievements(self, company) -> List[dict]:
        """获取所有成就状态"""
        unlocked = set(company.achievements)
        result = []
        
        for aid, achievement in self.achievements.items():
            result.append({
                "id": achievement.id,
                "name": achievement.name,
                "description": achievement.description,
                "icon": achievement.icon,
                "category": achievement.category,
                "unlocked": aid in unlocked,
            })
        
        return result
    
    def get_progress(self, company, achievement_id: str) -> dict:
        """获取成就进度"""
        achievement = self.achievements.get(achievement_id)
        if not achievement:
            return {"error": "Achievement not found"}
        
        unlocked = achievement_id in company.achievements
        progress = 0.0
        
        # 根据成就 ID 计算进度
        progress_map = {
            "first_project": (company.projects_completed, 1),
            "ten_projects": (company.projects_completed, 10),
            "fifty_projects": (company.projects_completed, 50),
            "hundred_projects": (company.projects_completed, 100),
            "hundred_days": (company.day, 100),
            "three_sixty_five_days": (company.day, 365),
            "seven_thirty_days": (company.day, 730),
            "brand_lv1": (company.brand_level, 1),
            "brand_lv2": (company.brand_level, 2),
            "brand_lv3": (company.brand_level, 3),
            "brand_lv4": (company.brand_level, 4),
            "brand_lv5": (company.brand_level, 5),
            "first_hire": (len(company.agents), 1),
            "ten_agents": (len(company.agents), 10),
            "hundred_agents": (len(company.agents), 100),
            "first_equipment": (len(company.equipments), 1),
            "all_equipment": (len(company.equipments), 5),
            "first_earnings": (company.total_earnings, 100000),
            "million_club": (company.total_earnings, 1000000),
            "ten_million": (company.total_earnings, 10000000),
        }
        
        if achievement_id in progress_map:
            current, target = progress_map[achievement_id]
            progress = min(100, (current / target) * 100) if target > 0 else 0
        
        # 已解锁成就进度为 100%
        if unlocked:
            progress = 100.0
        
        return {
            "id": achievement_id,
            "name": achievement.name,
            "icon": achievement.icon,
            "unlocked": unlocked,
            "progress": progress,
        }
