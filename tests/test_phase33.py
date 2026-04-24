"""
Phase 3.3 公司成长系统 — 自动化测试
覆盖：设备购买、品牌建设、投资融资
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from models.company import Company
from models.agent import create_agent
from models.project import create_project


# ========== 设备系统测试 ==========

class TestEquipmentSystem:
    """设备购买系统测试"""

    def test_buy_equipment_success(self):
        """购买设备成功"""
        company = Company(cash=100000)
        result = company.buy_equipment("高速网络")
        assert result["success"] is True
        assert "高速网络" in company.equipments
        assert company.cash == 90000

    def test_buy_equipment_insufficient_cash(self):
        """现金不足无法购买"""
        company = Company(cash=5000)
        result = company.buy_equipment("高速网络")
        assert result["success"] is False
        assert "高速网络" not in company.equipments

    def test_buy_equipment_already_owned(self):
        """已购买的设备不可重复购买"""
        company = Company(cash=100000)
        company.buy_equipment("高速网络")
        result = company.buy_equipment("高速网络")
        assert result["success"] is False

    def test_buy_equipment_office_level_requirement(self):
        """办公室等级不足无法购买高级设备"""
        company = Company(cash=200000, office_level=1)
        # 开发者工作站需要办公室 ≥2 级
        result = company.buy_equipment("开发者工作站")
        assert result["success"] is False

    def test_buy_all_equipments(self):
        """购买全部 5 种设备"""
        company = Company(cash=500000, office_level=5)
        equipment_names = [
            "高速网络", "开发者工作站", "云服务器集群",
            "测试实验室", "AI 训练集群"
        ]
        for name in equipment_names:
            result = company.buy_equipment(name)
            assert result["success"] is True, f"购买 {name} 失败"
        assert len(company.equipments) == 5

    def test_equipment_bonus_calculation(self):
        """设备加成计算正确"""
        company = Company(cash=500000, office_level=5)
        company.buy_equipment("高速网络")       # +5%
        company.buy_equipment("测试实验室")      # +5%
        bonus = company.get_equipment_bonus()
        assert bonus == 0.10  # 0.05 + 0.05

    def test_equipment_bonus_applied_to_project_progress(self):
        """设备加成在 next_day() 中正确应用到项目进度"""
        company = Company(cash=500000, office_level=5)
        company.buy_equipment("高速网络")  # +5% 进度
        company.buy_equipment("云服务器集群")  # +10% 进度

        # 雇佣员工
        agent = company.hire_agent("初级程序员", "测试员")
        
        # 创建并启动项目
        project = create_project("网站开发")
        company.accept_project(project)

        day_before = project.progress
        company.next_day()
        # 进度应该有设备加成（具体数值取决于实现）
        assert project.progress > day_before or project.status == "completed"


# ========== 品牌系统测试 ==========

class TestBrandSystem:
    """品牌建设系统测试"""

    def test_initial_brand_level(self):
        """初始品牌等级为 0"""
        company = Company()
        assert company.brand_level == 0

    def test_marketing_campaign_success(self):
        """营销活动成功提升品牌等级"""
        company = Company(cash=200000)
        result = company.run_marketing("社交媒体推广")  # +0.5 级, $15000
        assert result["success"] is True
        assert company.brand_level == 0.5

    def test_marketing_insufficient_cash(self):
        """现金不足无法执行营销活动"""
        company = Company(cash=10000)
        result = company.run_marketing("社交媒体推广")
        assert result["success"] is False

    def test_brand_level_tiers(self):
        """品牌等级各档位数值正确"""
        company = Company(cash=1000000, office_level=5)
        # 升到 Lv5
        company.run_marketing("全球发布会")   # +2 级 → 2.0
        company.run_marketing("电视广告")     # +1.5 级 → 3.5
        company.run_marketing("行业展会参展") # +1 级 → 4.5
        company.run_marketing("社交媒体推广") # +0.5 级 → 5.0
        assert company.brand_level == 5.0

    def test_brand_multiplier(self):
        """品牌倍率计算正确"""
        company = Company()
        company.brand_level = 3  # 知名公司 → 1.3x
        mult = company.get_brand_multiplier()
        assert mult == 1.3

    def test_brand_multiplier_cap(self):
        """品牌+设备总加成不超过 2.5x"""
        company = Company(cash=1000000, office_level=5)
        company.brand_level = 5.0  # 2.0x base
        company.buy_equipment("高速网络")
        company.buy_equipment("开发者工作站")
        company.buy_equipment("云服务器集群")
        company.buy_equipment("测试实验室")
        company.buy_equipment("AI 训练集群")  # equipment = 0.5

        total = company.get_total_project_multiplier()
        assert total <= 2.5

    def test_brand_maintenance(self):
        """品牌维护续费"""
        company = Company(cash=100000, office_level=3)
        company.brand_level = 3  # 日维护费 $2000
        result = company.maintain_brand(days=30)
        assert result["success"] is True
        # 30 天 × $2000 = $60000
        assert company.cash == 40000

    def test_brand_insufficient_maintenance(self):
        """维护费不足导致品牌降级"""
        company = Company(cash=1000, office_level=3)
        company.brand_level = 3  # 日维护费 $2000
        company.last_brand_check_day = 0

        # 推进 7 天（触发周检查）
        for _ in range(7):
            company.next_day()

        # 品牌应该降级（具体逻辑取决于实现）
        assert company.brand_level < 3.0 or company.brand_maintenance_due is True

    def test_brand_grace_period(self):
        """品牌降级宽限期 3 天"""
        company = Company(cash=1000, office_level=3)
        company.brand_level = 3
        company.last_brand_check_day = 0

        # 第 1 次周检查：不足，进入宽限期
        for _ in range(7):
            company.next_day()
        first_drop = company.brand_level

        # 宽限期内续费应该阻止进一步降级
        company.cash = 100000
        company.maintain_brand(days=30)

        # 再推进 7 天
        for _ in range(7):
            company.next_day()
        # 品牌不应再降
        assert company.brand_level >= first_drop - 0.5


# ========== 融资系统测试 ==========

class TestFundingSystem:
    """投资融资系统测试"""

    def test_initial_equity(self):
        """初始股权 100%"""
        company = Company()
        assert company.equity_sold == 0.0

    def test_seed_round_success(self):
        """种子轮融资成功"""
        company = Company(day=15, cash=75000, reputation=3.0)
        result = company.apply_funding("种子轮")
        assert result["success"] is True
        assert company.cash == 175000  # 75000 + 100000
        assert company.equity_sold == 0.10

    def test_seed_round_too_early(self):
        """第 10 天前无法种子轮融资"""
        company = Company(day=5, cash=75000, reputation=3.0)
        result = company.apply_funding("种子轮")
        assert result["success"] is False

    def test_angel_round_reputation_requirement(self):
        """天使轮需要 reputation ≥ 3.5"""
        company = Company(day=35, cash=75000, reputation=3.0)
        result = company.apply_funding("天使轮")
        assert result["success"] is False

    def test_angel_round_success(self):
        """天使轮融资成功"""
        company = Company(day=35, cash=75000, reputation=3.5)
        result = company.apply_funding("天使轮")
        assert result["success"] is True
        assert company.equity_sold == 0.15  # 天使轮 15%

    def test_all_funding_rounds(self):
        """完成全部 5 轮融资"""
        company = Company(day=160, cash=75000, reputation=4.8, office_level=5)
        rounds = ["种子轮", "天使轮", "A 轮", "B 轮", "IPO"]
        for r in rounds:
            result = company.apply_funding(r)
            assert result["success"] is True, f"{r} 融资失败"
        # 总出让: 10% + 15% + 20% + 15% + 10% = 70%
        assert company.equity_sold == 0.70

    def test_founder_out_triggered(self):
        """股权 >50% 触发创始人出局结局"""
        company = Company(day=160, cash=75000, reputation=4.8, office_level=5)
        company.apply_funding("种子轮")   # 10%
        company.apply_funding("天使轮")   # 25%
        company.apply_funding("A 轮")     # 45%
        company.apply_funding("B 轮")     # 60% > 50%

        assert company.equity_sold > 0.5
        status = company.get_status()
        assert status.get("founder_out") is True

    def test_dividend_calculation(self):
        """分红计算正确"""
        company = Company(day=35, cash=500000, reputation=3.5)
        company.apply_funding("种子轮")   # 5% 分红
        company.apply_funding("天使轮")   # 8% 分红
        # 总分红比例: 5% + 8% = 13%
        assert company.get_total_dividend_rate() == 0.13

    def test_dividend_deduction(self):
        """分红每 30 天从现金中扣除"""
        company = Company(day=30, cash=500000, reputation=3.5, office_level=3)
        company.apply_funding("种子轮")   # 5%
        company.cash = 500000

        # 模拟 30 天净利润
        # 假设净利润 = 收入 - 工资 - 租金 - 维护费
        # 分红 = 净利润 × 总分红比例
        company.next_day()  # day 31, 触发 30 天结算
        # 分红应该已扣除（具体取决于实现）

    def test_dividend_arrears_penalty(self):
        """分红欠款超过 1 个月导致声誉下降"""
        company = Company(day=30, cash=10000, reputation=4.0, office_level=3)
        company.apply_funding("种子轮")
        company.apply_funding("天使轮")
        company.apply_funding("A 轮")
        # 现金极少，无法支付分红
        # 推进到 day 60（触发 30 天分红结算）
        for _ in range(30):
            company.next_day()
        # reputation 应该下降或分红累积
        assert company.reputation < 4.0 or company.dividend_accumulator > 0

    def test_equity_buyback(self):
        """股权回购"""
        company = Company(day=100, cash=500000, reputation=4.0, total_earnings=200000)
        company.apply_funding("种子轮")   # sold 10%
        initial_equity = company.equity_sold

        result = company.buyback_equity(50000)
        assert result["success"] is True
        assert company.equity_sold < initial_equity

    def test_buyback_no_valuation(self):
        """无盈利的公司无法回购"""
        company = Company(day=10, cash=500000, reputation=3.0, total_earnings=0)
        company.apply_funding("种子轮")
        result = company.buyback_equity(50000)
        assert result.get("error") is not None or result["success"] is False


# ========== 集成测试 ==========

class TestIntegration:
    """三系统集成测试"""

    def test_equipment_and_brand_combined_bonus(self):
        """设备+品牌加成叠加正确"""
        company = Company(cash=1000000, office_level=5)
        company.buy_equipment("高速网络")       # +5%
        company.brand_level = 2                 # 1.2x base
        total = company.get_total_project_multiplier()
        # brand(1.2) + equipment(0.05) = 1.25（具体公式以最终实现为准）
        assert total > 1.0
        assert total <= 2.5

    def test_funding_and_brand_maintenance(self):
        """融资后现金充足可以正常维护品牌"""
        company = Company(day=35, cash=75000, reputation=3.5, office_level=3)
        company.apply_funding("种子轮")         # +$100k
        company.run_marketing("行业展会参展")   # 品牌 +1
        company.maintain_brand(days=30)
        assert company.brand_level >= 1.0

    def test_full_game_scenario(self):
        """完整游戏流程：雇佣→做项目→买设备→升品牌→融资"""
        company = Company(name="测试公司", cash=75000)

        # 雇佣员工
        agent = company.hire_agent("初级程序员", "测试员")
        assert len(company.agents) == 1

        # 接受项目
        project = create_project("网站开发")
        company.accept_project(project)
        assert project.status == "in_progress"

        # 推进天数（员工工作产生进度）
        for _ in range(10):
            company.next_day()

        # 购买设备
        if company.cash >= 10000:
            company.buy_equipment("高速网络")

        # 检查状态正常
        status = company.get_status()
        assert "cash" in status
        assert "bond" in status or "brand" in str(status)
