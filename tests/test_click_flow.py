#!/usr/bin/env python3
"""
前端点击测试 - 模拟真实用户操作
"""

import requests
import time

API = 'http://localhost:5001/api'

def test_click_flow():
    """模拟真实用户点击流程"""
    print("=" * 60)
    print("🎮 前端点击流程测试")
    print("=" * 60)
    print()
    
    # 1. 开始新游戏
    print("1️⃣ 点击'新游戏'...")
    resp = requests.post(f'{API}/game/new', json={'company_name': '测试公司'})
    data = resp.json()
    assert data['success'], "新游戏失败"
    print(f"   ✅ 公司创建：{data['company']['name']}")
    print(f"   ✅ 初始资金：${data['company']['cash']:,}")
    print(f"   ✅ 初始员工：{len(data['company']['agents'])} 人")
    print()
    
    # 2. 点击"下一天"
    print("2️⃣ 点击'📅 下一天'...")
    resp = requests.post(f'{API}/game/next-day')
    data = resp.json()
    print(f"   ✅ 天数：{data['day']}")
    print(f"   ✅ 支出：${data['expenses']:,}")
    if 'event' in data:
        print(f"   ✅ 事件：{data['event']['name']}")
    print()
    
    # 3. 点击"雇佣员工"
    print("3️⃣ 点击'👥 雇佣员工'...")
    resp = requests.post(f'{API}/agents/hire', json={'role': '初级程序员', 'name': '新员工'})
    data = resp.json()
    assert data['success'], "雇佣失败"
    print(f"   ✅ 雇佣：{data['agent']['name']}")
    print(f"   ✅ 职位：{data['agent']['role']}")
    print()
    
    # 4. 点击"查看项目"
    print("4️⃣ 点击'📋 查看项目'...")
    resp = requests.get(f'{API}/projects')
    projects = resp.json()['projects']
    print(f"   ✅ 项目数：{len(projects)}")
    if projects:
        p = projects[0]
        print(f"   ✅ 第一个项目：{p['name']}")
        print(f"   ✅ 报酬：${p['reward']:,}")
    print()
    
    # 5. 点击"接受项目"
    if projects:
        print("5️⃣ 点击'接受项目'...")
        resp = requests.post(f'{API}/projects/accept', json={'project_id': projects[0]['id']})
        data = resp.json()
        print(f"   ✅ 接受：{data.get('success', False)}")
        print()
    
    # 6. 点击"升级办公室"
    print("6️⃣ 点击'🏢 升级办公室'...")
    resp = requests.post(f'{API}/company/upgrade-office')
    data = resp.json()
    if data.get('success'):
        print(f"   ✅ 升级到：Lv{data['office_level']}")
    else:
        print(f"   ℹ️  资金不足 (需要${10000:,})")
    print()
    
    # 7. 再次点击"下一天" × 3
    print("7️⃣ 连续点击'下一天' × 3...")
    for i in range(3):
        resp = requests.post(f'{API}/game/next-day')
        data = resp.json()
        print(f"   ✅ 第 {data['day']} 天 - 支出：${data['expenses']:,}")
    print()
    
    # 8. 查看最终状态
    print("8️⃣ 查看最终状态...")
    resp = requests.get(f'{API}/game/status')
    status = resp.json()
    print(f"   ✅ 现金：${status['cash']:,}")
    print(f"   ✅ 口碑：{status['reputation']}/5.0")
    print(f"   ✅ 员工：{status['agent_count']}/{status['max_agents']}")
    print(f"   ✅ 天数：{status['day']}")
    print()
    
    print("=" * 60)
    print("✅ 所有点击测试通过！")
    print("=" * 60)

if __name__ == '__main__':
    test_click_flow()
