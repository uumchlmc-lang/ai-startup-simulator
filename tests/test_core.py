#!/usr/bin/env python3
"""
AI 创业模拟器 - 后端核心测试
"""

import sys
sys.path.insert(0, "/Users/cq109911/.openclaw/workspace-car-export/ai-startup-simulator")

from backend.models import Agent, Project, Company
from backend.services import GameEngine


def test_agent():
    """测试 Agent 模型"""
    print("=" * 60)
    print("测试 Agent 模型")
    print("=" * 60)
    
    agent = Agent(name="测试 Agent", role="程序员", efficiency=80)
    print(f"✅ 创建 Agent: {agent.name}")
    print(f"   效率：{agent.efficiency}")
    print(f"   薪资：${agent.salary}")
    
    progress = agent.work(8)
    print(f"✅ 工作 8 小时，贡献进度：{progress}")
    
    agent.rest()
    print(f"✅ 休息后满意度：{agent.satisfaction}")
    
    print()


def test_project():
    """测试 Project 模型"""
    print("=" * 60)
    print("测试 Project 模型")
    print("=" * 60)
    
    project = Project(name="测试项目", difficulty=2, reward=15000)
    print(f"✅ 创建项目：{project.name}")
    print(f"   难度：⭐{project.difficulty}")
    print(f"   报酬：${project.reward}")
    
    project.start()
    print(f"✅ 项目状态：{project.status}")
    
    project.update_progress(50)
    print(f"✅ 进度更新：{project.progress}%")
    
    print()


def test_company():
    """测试 Company 模型"""
    print("=" * 60)
    print("测试 Company 模型")
    print("=" * 60)
    
    company = Company(name="测试公司")
    print(f"✅ 创建公司：{company.name}")
    print(f"   初始资金：${company.cash}")
    print(f"   口碑：{company.reputation}/5.0")
    
    # 雇佣 Agent
    agent = company.hire_agent("初级程序员", "小王")
    print(f"✅ 雇佣 Agent: {agent.name}")
    print(f"   每日薪资：${company.get_agent_daily_salary()}")
    
    # 创建项目
    from backend.models import create_project
    project = create_project("网站开发")
    company.projects.append(project)
    print(f"✅ 创建项目：{project.name}")
    
    print()


def test_game_engine():
    """测试游戏引擎"""
    print("=" * 60)
    print("测试游戏引擎")
    print("=" * 60)
    
    engine = GameEngine()
    
    # 新游戏
    company = engine.new_game("我的 AI 公司")
    print(f"✅ 新游戏开始：{company.name}")
    print(f"   初始资金：${company.cash}")
    print(f"   初始 Agent 数：{len(company.agents)}")
    
    # 获取状态
    status = engine.get_company_status()
    print(f"✅ 公司状态:")
    print(f"   天数：{status['day']}")
    print(f"   口碑：{status['reputation']}")
    
    # 下一天
    result = engine.next_day()
    print(f"✅ 下一天结算:")
    print(f"   支出：${result['expenses']}")
    if 'event' in result:
        print(f"   事件：{result['event']['name']}")
    
    # 保存
    success = engine.save_game("test-save")
    print(f"✅ 保存游戏：{'成功' if success else '失败'}")
    
    print()


def main():
    """运行所有测试"""
    print("\n")
    print("🎮" * 30)
    print("AI 创业模拟器 - 后端核心测试")
    print("🎮" * 30)
    print("\n")
    
    try:
        test_agent()
        test_project()
        test_company()
        test_game_engine()
        
        print("=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
        return 0
    
    except Exception as e:
        print("=" * 60)
        print(f"❌ 测试失败：{e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
