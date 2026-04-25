"""
Phase 3.4 成就系统 - 自动化测试
覆盖：成就定义、检查引擎、进度追踪、API
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from models.company import Company
from models.agent import create_agent
from models.project import create_project
from services.achievement_engine import AchievementEngine, ACHIEVEMENTS


class TestAchievementDefinitions:
    """成就定义测试"""

    def test_total_achievements_count(self):
        """成就总数为 52"""
        assert len(ACHIEVEMENTS) == 52

    def test_categories(self):
        """成就分类正确"""
        categories = set()
        for achievement in ACHIEVEMENTS.values():
            categories.add(achievement.category)
        
        expected_categories = {"成长", "项目", "团队", "设备", "品牌", "融资", "财务", "隐藏"}
        assert categories == expected_categories

    def test_hidden_achievements_count(self):
        """隐藏成就数量为 6"""
        hidden = [a for a in ACHIEVEMENTS.values() if a.category == "隐藏"]
        assert len(hidden) == 6

    def test_all_achievements_have_required_fields(self):
        """所有成就都有必要字段"""
        for aid, achievement in ACHIEVEMENTS.items():
            assert achievement.id == aid
            assert achievement.name
            assert achievement.description
            assert achievement.icon
            assert achievement.category
            assert callable(achievement.condition)


class TestAchievementEngine:
    """成就检查引擎测试"""

    def test_first_hire_achievement(self):
        """雇佣第一个员工解锁成就"""
        company = Company()
        company.hire_agent("初级程序员", "测试员")
        
        engine = AchievementEngine()
        new_unlocks = engine.check_all(company)
        
        assert "first_hire" in new_unlocks

    def test_first_project_achievement(self):
        """完成第一个项目解锁成就"""
        company = Company(cash=75000)
        company.hire_agent("初级程序员", "测试员")
        
        project = create_project("网站开发")
        company.accept_project(project)
        
        # 模拟项目完成
        company.projects_completed = 1
        company.completed_project_types.add(project.type)
        
        engine = AchievementEngine()
        new_unlocks = engine.check_all(company)
        
        assert "first_project" in new_unlocks

    def test_first_equipment_achievement(self):
        """购买第一个设备解锁成就"""
        company = Company(cash=75000, office_level=1)
        company.buy_equipment("高速网络")
        
        engine = AchievementEngine()
        new_unlocks = engine.check_all(company)
        
        assert "first_equipment" in new_unlocks

    def test_brand_lv1_achievement(self):
        """品牌达到 Lv1 解锁成就"""
        company = Company(cash=75000)
        company.brand_level = 1.0
        
        engine = AchievementEngine()
        new_unlocks = engine.check_all(company)
        
        assert "brand_lv1" in new_unlocks

    def test_seed_round_achievement(self):
        """种子轮融资解锁成就"""
        company = Company(cash=75000, day=15, reputation=3.0)
        company.apply_funding("种子轮")
        
        engine = AchievementEngine()
        new_unlocks = engine.check_all(company)
        
        assert "seed_round" in new_unlocks

    def test_no_duplicate_unlocks(self):
        """已解锁成就不会重复解锁"""
        company = Company()
        company.hire_agent("初级程序员", "测试员")
        
        engine = AchievementEngine()
        new_unlocks1 = engine.check_all(company)
        new_unlocks2 = engine.check_all(company)
        
        assert "first_hire" in new_unlocks1
        assert "first_hire" not in new_unlocks2

    def test_check_category(self):
        """按分类检查成就"""
        company = Company(cash=75000)
        company.hire_agent("初级程序员", "测试员")
        
        engine = AchievementEngine()
        new_unlocks = engine.check_category(company, "团队")
        
        assert "first_hire" in new_unlocks

    def test_get_achievement(self):
        """获取成就信息"""
        engine = AchievementEngine()
        achievement = engine.get_achievement("first_project")
        
        assert achievement is not None
        assert achievement["id"] == "first_project"
        assert achievement["name"] == "迈出第一步"
        assert achievement["category"] == "成长"

    def test_get_nonexistent_achievement(self):
        """获取不存在的成就"""
        engine = AchievementEngine()
        achievement = engine.get_achievement("nonexistent")
        
        assert achievement is None


class TestAchievementProgress:
    """成就进度测试"""

    def test_projects_completed_progress(self):
        """项目完成进度计算"""
        company = Company(projects_completed=5)
        
        engine = AchievementEngine()
        progress = engine.get_progress(company, "ten_projects")
        
        assert progress["progress"] == 50.0  # 5/10 = 50%

    def test_day_progress(self):
        """天数进度计算"""
        company = Company(day=50)
        
        engine = AchievementEngine()
        progress = engine.get_progress(company, "hundred_days")
        
        assert progress["progress"] == 50.0  # 50/100 = 50%

    def test_brand_progress(self):
        """品牌进度计算"""
        company = Company(brand_level=2.5)
        
        engine = AchievementEngine()
        progress = engine.get_progress(company, "brand_lv5")
        
        assert progress["progress"] == 50.0  # 2.5/5 = 50%

    def test_agent_progress(self):
        """员工进度计算"""
        company = Company()
        for i in range(5):
            company.hire_agent("初级程序员", f"员工{i}")
        
        engine = AchievementEngine()
        progress = engine.get_progress(company, "ten_agents")
        
        assert progress["progress"] == 50.0  # 5/10 = 50%

    def test_equipment_progress(self):
        """设备进度计算"""
        company = Company(cash=500000, office_level=5)
        company.buy_equipment("高速网络")
        company.buy_equipment("开发者工作站")
        
        engine = AchievementEngine()
        progress = engine.get_progress(company, "all_equipment")
        
        assert progress["progress"] == 40.0  # 2/5 = 40%

    def test_unlocked_achievement_progress(self):
        """已解锁成就进度为 100%"""
        company = Company(projects_completed=1)
        
        engine = AchievementEngine()
        engine.check_all(company)  # 检查并解锁成就
        
        progress = engine.get_progress(company, "first_project")
        
        assert progress["unlocked"] is True
        assert progress["progress"] == 100.0


class TestAchievementAPI:
    """成就 API 测试"""

    def test_get_all_achievements(self):
        """获取所有成就"""
        company = Company()
        
        engine = AchievementEngine()
        achievements = engine.get_all_achievements(company)
        
        assert len(achievements) == 52
        for a in achievements:
            assert "id" in a
            assert "name" in a
            assert "description" in a
            assert "icon" in a
            assert "category" in a
            assert "unlocked" in a

    def test_get_unlocked_achievements(self):
        """获取已解锁成就"""
        company = Company()
        company.hire_agent("初级程序员", "测试员")
        
        engine = AchievementEngine()
        engine.check_all(company)
        
        unlocked = []
        for aid in company.achievements:
            achievement = engine.get_achievement(aid)
            if achievement:
                unlocked.append(achievement)
        
        assert len(unlocked) >= 1
        assert any(a["id"] == "first_hire" for a in unlocked)
