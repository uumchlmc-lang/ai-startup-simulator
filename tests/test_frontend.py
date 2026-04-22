#!/usr/bin/env python3
"""
前端功能自动化测试
"""

import requests
import json

API_BASE = 'http://localhost:5001/api'

def test(name, condition, expected=True):
    """测试断言"""
    status = "✅" if condition == expected else "❌"
    print(f"{status} {name}")
    if condition != expected:
        print(f"   期望：{expected}, 实际：{condition}")
    return condition == expected

def main():
    print("=" * 60)
    print("🎮 AI 创业模拟器 - 前端功能测试")
    print("=" * 60)
    print()
    
    passed = 0
    total = 0
    
    # 测试 1: 页面加载
    print("1️⃣ 页面加载测试")
    try:
        resp = requests.get('http://localhost:5001', timeout=5)
        total += 1
        if test("  状态码", resp.status_code, 200): passed += 1
        total += 1
        if test("  包含标题", "AI 创业模拟器" in resp.text): passed += 1
        total += 1
        if test("  包含现金显示", 'id="cash"' in resp.text): passed += 1
        total += 1
        if test("  包含下一天按钮", "下一天" in resp.text): passed += 1
    except Exception as e:
        print(f"❌ 页面加载失败：{e}")
    print()
    
    # 测试 2: 新游戏
    print("2️⃣ 新游戏测试")
    try:
        resp = requests.post(f'{API_BASE}/game/new', 
                           json={'company_name': '测试公司'}, 
                           timeout=5)
        data = resp.json()
        total += 1
        if test("  创建成功", data.get('success', False)): passed += 1
        total += 1
        if test("  初始资金", data['company']['cash'] == 50000): passed += 1
        total += 1
        if test("  初始员工数", len(data['company']['agents']) == 2): passed += 1
        total += 1
        if test("  初始口碑", data['company']['reputation'] == 3.0): passed += 1
    except Exception as e:
        print(f"❌ 新游戏失败：{e}")
    print()
    
    # 测试 3: 下一天
    print("3️⃣ 下一天测试")
    try:
        resp = requests.post(f'{API_BASE}/game/next-day', timeout=5)
        data = resp.json()
        total += 1
        if test("  天数增加", data.get('day', 0) == 1): passed += 1
        total += 1
        if test("  有支出", data.get('expenses', 0) > 0): passed += 1
        total += 1
        if test("  游戏未结束", not data.get('game_over', False)): passed += 1
    except Exception as e:
        print(f"❌ 下一天失败：{e}")
    print()
    
    # 测试 4: 员工列表
    print("4️⃣ 员工列表测试")
    try:
        resp = requests.get(f'{API_BASE}/agents', timeout=5)
        data = resp.json()
        total += 1
        if test("  返回列表", 'agents' in data): passed += 1
        total += 1
        if test("  员工数>=2", len(data.get('agents', [])) >= 2): passed += 1
    except Exception as e:
        print(f"❌ 员工列表失败：{e}")
    print()
    
    # 测试 5: 雇佣员工
    print("5️⃣ 雇佣员工测试")
    try:
        resp = requests.post(f'{API_BASE}/agents/hire', 
                           json={'role': '初级程序员', 'name': '测试员工'}, 
                           timeout=5)
        data = resp.json()
        total += 1
        if test("  雇佣成功", data.get('success', False)): passed += 1
        total += 1
        if test("  员工名字", data.get('agent', {}).get('name') == '测试员工'): passed += 1
    except Exception as e:
        print(f"❌ 雇佣失败：{e}")
    print()
    
    # 测试 6: 项目列表
    print("6️⃣ 项目列表测试")
    try:
        resp = requests.get(f'{API_BASE}/projects', timeout=5)
        data = resp.json()
        total += 1
        if test("  返回列表", 'projects' in data): passed += 1
        total += 1
        if test("  有项目", len(data.get('projects', [])) > 0): passed += 1
    except Exception as e:
        print(f"❌ 项目列表失败：{e}")
    print()
    
    # 测试 7: 接受项目
    print("7️⃣ 接受项目测试")
    try:
        # 先获取项目
        resp = requests.get(f'{API_BASE}/projects', timeout=5)
        projects = resp.json().get('projects', [])
        if projects:
            project_id = projects[0]['id']
            resp = requests.post(f'{API_BASE}/projects/accept', 
                               json={'project_id': project_id}, 
                               timeout=5)
            data = resp.json()
            total += 1
            if test("  接受成功", data.get('success', False)): passed += 1
        else:
            print("⚠️  无可用项目")
    except Exception as e:
        print(f"❌ 接受项目失败：{e}")
    print()
    
    # 测试 8: 游戏状态
    print("8️⃣ 游戏状态测试")
    try:
        resp = requests.get(f'{API_BASE}/game/status', timeout=5)
        data = resp.json()
        total += 1
        if test("  返回状态", 'cash' in data): passed += 1
        total += 1
        if test("  天数>0", data.get('day', 0) > 0): passed += 1
        total += 1
        if test("  员工数>0", data.get('agent_count', 0) > 0): passed += 1
    except Exception as e:
        print(f"❌ 游戏状态失败：{e}")
    print()
    
    # 总结
    print("=" * 60)
    print(f"测试结果：{passed}/{total} 通过 ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    exit(main())
