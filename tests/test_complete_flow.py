#!/usr/bin/env python3
"""
AI 创业模拟器 - 完整功能测试
模拟真实用户操作流程
"""

from playwright.sync_api import sync_playwright
import time

def test_complete_game_flow():
    """完整游戏流程测试"""
    
    print("=" * 70)
    print("🎮 AI 创业模拟器 - 完整功能测试")
    print("=" * 70)
    print()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器
        page = browser.new_page()
        
        # 捕获错误
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        
        # ========== 1. 打开页面 ==========
        print("📋 测试 1: 打开页面")
        print("-" * 70)
        page.goto('http://localhost:5001')
        page.wait_for_load_state('networkidle')
        time.sleep(2)
        
        # 检查标题
        title = page.title()
        print(f"✅ 页面标题：{title}")
        assert title == "🎮 AI 创业模拟器", f"标题错误：{title}"
        
        # 检查初始状态
        cash = page.locator('#cash').inner_text()
        day = page.locator('#day').inner_text()
        agents = page.locator('#agents').inner_text()
        reputation = page.locator('#reputation').inner_text()
        
        print(f"✅ 初始资金：{cash}")
        print(f"✅ 初始天数：{day}")
        print(f"✅ 初始员工：{agents}")
        print(f"✅ 初始口碑：{reputation}")
        assert cash == "$50,000", f"初始资金错误：{cash}"
        assert day == "0", f"初始天数错误：{day}"
        print()
        
        # ========== 2. 查看项目 ==========
        print("📋 测试 2: 查看项目")
        print("-" * 70)
        page.click('button:has-text("查看项目")')
        time.sleep(1)
        
        # 检查项目标签页
        projects_tab = page.locator('#tab-projects')
        assert projects_tab.is_visible(), "项目标签页未显示"
        print("✅ 项目标签页显示")
        
        # 检查项目列表
        projects_list = page.locator('#projects-list')
        assert projects_list.is_visible(), "项目列表未显示"
        print("✅ 项目列表显示")
        
        # 检查项目卡片
        project_cards = page.locator('.card')
        count = project_cards.count()
        print(f"✅ 项目数量：{count}")
        assert count >= 1, "没有可用项目"
        
        # 检查接受按钮
        accept_btn = page.locator('button:has-text("接受")')
        print(f"✅ 接受按钮：{accept_btn.count()}个")
        print()
        
        # ========== 3. 接受项目 ==========
        print("📋 测试 3: 接受项目")
        print("-" * 70)
        accept_btn.first.click()
        time.sleep(2)
        
        # 检查通知
        notifications = page.locator('.notification')
        assert notifications.count() > 0, "没有通知"
        notif_text = notifications.first.inner_text()
        print(f"✅ 通知：{notif_text[:50]}...")
        assert "✅" in notif_text or "接受" in notif_text, f"通知内容错误：{notif_text}"
        print()
        
        # ========== 4. 查看员工 ==========
        print("📋 测试 4: 查看员工")
        print("-" * 70)
        page.click('button:has-text("雇佣员工")')
        time.sleep(1)
        
        # 检查员工标签页
        agents_tab = page.locator('#tab-agents')
        assert agents_tab.is_visible(), "员工标签页未显示"
        print("✅ 员工标签页显示")
        
        # 检查员工列表
        agents_list = page.locator('#agents-list')
        assert agents_list.is_visible(), "员工列表未显示"
        print("✅ 员工列表显示")
        
        # 检查员工卡片
        agent_cards = page.locator('#agents-list .card')
        agent_count = agent_cards.count()
        print(f"✅ 员工数量：{agent_count}")
        
        # 检查员工信息
        if agent_count > 0:
            first_agent = agent_cards.first.inner_text()
            print(f"✅ 第一个员工：{first_agent[:50]}...")
        print()
        
        # ========== 5. 雇佣新员工 ==========
        print("📋 测试 5: 雇佣员工")
        print("-" * 70)
        
        # 选择职位
        page.select_option('#hire-role', '初级程序员')
        print("✅ 选择职位：初级程序员")
        
        # 点击雇佣
        page.click('button:has-text("雇佣")')
        time.sleep(3)
        
        # 检查通知
        notifications = page.locator('.notification')
        if notifications.count() > 0:
            notif_text = notifications.first.inner_text()
            print(f"✅ 通知：{notif_text[:50]}...")
        else:
            print("ℹ️  通知已消失")
        
        # 检查员工数变化
        new_agents = page.locator('#agents').inner_text()
        print(f"✅ 员工数：{new_agents}")
        print()
        
        # ========== 6. 下一天 ==========
        print("📋 测试 6: 下一天")
        print("-" * 70)
        
        old_day = page.locator('#day').inner_text()
        old_cash = page.locator('#cash').inner_text()
        
        page.click('button:has-text("下一天")')
        time.sleep(2)
        
        new_day = page.locator('#day').inner_text()
        new_cash = page.locator('#cash').inner_text()
        
        print(f"✅ 天数：{old_day} → {new_day}")
        print(f"✅ 现金：{old_cash} → {new_cash}")
        assert int(new_day) == int(old_day) + 1, f"天数错误：{new_day}"
        
        # 检查通知
        notifications = page.locator('.notification')
        notif_text = notifications.first.inner_text()
        print(f"✅ 通知：{notif_text[:50]}...")
        print()
        
        # ========== 7. 检查项目进度 ==========
        print("📋 测试 7: 检查项目进度")
        print("-" * 70)
        page.click('button:has-text("查看项目")')
        time.sleep(1)
        
        # 检查进度条
        progress_bars = page.locator('.progress-fill')
        count = progress_bars.count()
        print(f"✅ 项目数量：{count}")
        
        # 检查第一个项目的进度
        if count > 0:
            first_bar = progress_bars.first
            style = first_bar.get_attribute('style')
            print(f"✅ 进度条样式：{style}")
            
            # 检查是否有可交付的项目
            complete_btn = page.locator('button:has-text("交付")')
            if complete_btn.count() > 0:
                print(f"✅ 可交付项目：{complete_btn.count()}个")
                print("✅ 项目进度正常！")
        print()
        
        # ========== 8. 升级办公室 ==========
        print("📋 测试 8: 升级办公室")
        print("-" * 70)
        
        page.click('button:has-text("升级办公室")')
        time.sleep(1)
        
        # 检查通知
        notifications = page.locator('.notification')
        notif_text = notifications.first.inner_text()
        print(f"✅ 通知：{notif_text[:50]}...")
        print()
        
        # ========== 9. 再下一天 ==========
        print("📋 测试 9: 再下一天")
        print("-" * 70)
        
        page.click('button:has-text("下一天")')
        time.sleep(2)
        
        final_day = page.locator('#day').inner_text()
        final_cash = page.locator('#cash').inner_text()
        print(f"✅ 天数：{final_day}")
        print(f"✅ 现金：{final_cash}")
        print()
        
        # ========== 10. 检查项目是否可交付 ==========
        print("📋 测试 10: 检查项目交付")
        print("-" * 70)
        page.click('button:has-text("查看项目")')
        time.sleep(1)
        
        # 检查是否有交付按钮
        complete_btn = page.locator('button:has-text("交付")')
        if complete_btn.count() > 0:
            print(f"✅ 交付按钮：{complete_btn.count()}个")
            print("✅ 项目可以交付！")
        else:
            print("ℹ️  项目进度不足，需要继续工作")
        print()
        
        # ========== 截图 ==========
        print("📋 截图")
        print("-" * 70)
        page.screenshot(path='/tmp/game-complete-test.png', full_page=True)
        print("✅ 截图已保存：/tmp/game-complete-test.png")
        print()
        
        # ========== 错误检查 ==========
        print("📋 错误检查")
        print("-" * 70)
        if errors:
            print(f"❌ 发现 {len(errors)} 个错误:")
            for err in errors:
                print(f"   - {err}")
        else:
            print("✅ 没有错误")
        print()
        
        browser.close()
        
        # ========== 最终结果 ==========
        print("=" * 70)
        if not errors and int(final_day) >= 2:
            print("✅ 所有测试通过！游戏功能完整！")
        else:
            print("❌ 测试失败")
        print("=" * 70)
        print()

if __name__ == '__main__':
    test_complete_game_flow()
