/**
 * 主应用逻辑
 */

import * as api from './api.js';

// 当前状态
let gameState = null;

// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎮 AI 创业模拟器启动...');
    
    // 尝试加载游戏
    const loaded = await api.loadGame();
    if (loaded && loaded.success) {
        console.log('✅ 游戏已加载');
        updateUI(loaded.company);
        // 加载员工和项目列表
        setTimeout(() => {
            updateAgentsList();
            updateProjectsList();
        }, 500);
    } else {
        console.log('ℹ️ 开始新游戏');
        await startNewGame();
    }
    
    showNotification('🎮 欢迎来到 AI 创业模拟器！', 'info');
});

// 开始新游戏
async function startNewGame() {
    const result = await api.newGame();
    if (result.success) {
        gameState = result.company;
        updateUI(gameState);
        showNotification('✅ 新游戏开始！', 'success');
    }
}

// 下一天
async function nextDay() {
    const btn = window.event ? window.event.target : document.querySelector('button:has-text("下一天")');
    btn.disabled = true;
    btn.textContent = '⏳ 处理中...';
    
    try {
        const result = await api.nextDay();
        
        if (result.error) {
            showNotification(`❌ 错误：${result.error}`, 'error');
            return;
        }
        
        const status = await api.getGameStatus();
        updateUI(status);
        showDayResult(result);
        
        if (result.game_over) {
            showGameOver(result);
        }
    } catch (e) {
        showNotification(`❌ 错误：${e.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = '📅 下一天';
    }
}

// 显示当日结算
function showDayResult(result) {
    let msg = `📅 第 ${result.day} 天结算\n`;
    msg += `💵 支出：$${(result.expenses || 0).toLocaleString()}`;
    
    if (result.income > 0) {
        msg += `\n💰 收入：$${result.income.toLocaleString()}`;
    }
    
    if (result.event) {
        const emoji = result.event.type === 'positive' ? '✅' : '❌';
        msg += `\n${emoji} 事件：${result.event.name}`;
    }
    
    showNotification(msg, 'info');
}

// 游戏结束
function showGameOver(result) {
    const modal = document.getElementById('game-over');
    const title = document.getElementById('game-over-title');
    const reason = document.getElementById('game-over-reason');
    
    title.textContent = result.game_over_reason === 'bankruptcy' ? '💸 破产！' : '⭐ 倒闭！';
    reason.textContent = result.game_over_reason === 'bankruptcy'
        ? '公司现金低于 -$50k！'
        : '公司口碑降至 0！';
    
    modal.style.display = 'flex';
}

// 重新开始
async function newGame() {
    document.getElementById('game-over').style.display = 'none';
    await startNewGame();
}

// 升级办公室
async function upgradeOffice() {
    // 获取当前办公室等级和升级成本
    const status = await api.getGameStatus();
    const currentLevel = status.office_level || 1;
    const nextLevel = currentLevel + 1;
    
    // 计算升级成本 (每级$50k)
    const upgradeCost = currentLevel * 50000;
    
    if (currentLevel >= 5) {
        showNotification('❌ 办公室已达最高等级！', 'error');
        return;
    }
    
    // 确认对话框
    if (!confirm(`🏢 升级办公室

当前等级：Lv${currentLevel}
目标等级：Lv${nextLevel}
升级成本：$${upgradeCost.toLocaleString()}

升级效果:
• 员工容量 +5
• 培训效果 +${currentLevel * 5}%
• 每日租金 +$${(currentLevel * 1000).toLocaleString()}

确定升级吗？`)) {
        return;
    }
    
    try {
        const result = await api.upgradeOffice();
        if (result.success) {
            showNotification(`✅ 升级到 Lv${result.office_level}！花费 $${upgradeCost.toLocaleString()}`, 'success');
            const newStatus = await api.getGameStatus();
            updateUI(newStatus);
        } else {
            showNotification(`❌ ${result.error || '资金不足'}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ 错误：${e.message}`, 'error');
    }
}

// 雇佣员工
async function hireAgent() {
    const role = document.getElementById('hire-role').value;
    try {
        const result = await api.hireAgent(role);
        if (result.success) {
            showNotification(`✅ 雇佣了 ${result.agent.name}！`, 'success');
            updateAgentsList();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ 错误：${e.message}`, 'error');
    }
}

// 解雇员工
window.fireAgent = async function(agentId, agentName) {
    if (!confirm(`确定要解雇 ${agentName} 吗？\n\n解雇后无法恢复！`)) {
        return;
    }
    try {
        const result = await api.fireAgent(agentId);
        if (result.success) {
            showNotification(`✅ 已解雇 ${agentName}`, 'success');
            updateAgentsList();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
};

// 培训员工
window.trainAgent = async function(agentId, agentName) {
    const TRAINING_TYPES = {
        'online': { name: '在线课程', days: 1, cost: 500, points: 2 },
        'workshop': { name: '工作坊', days: 3, cost: 1500, points: 5 },
        'external': { name: '外部培训', days: 5, cost: 3000, points: 10 },
        'conference': { name: '行业会议', days: 7, cost: 5000, points: 15 },
        'mentor': { name: '导师指导', days: 10, cost: 8000, points: 20 },
    };
    
    // 创建选择对话框
    const options = Object.entries(TRAINING_TYPES).map(([key, value]) => 
        `${key}|${value.name} - ${value.days}天 - $${value.cost.toLocaleString()} (+${value.points}技能点)`
    ).join('\n');
    
    const choice = prompt(`📚 选择培训类型 - ${agentName}\n\n${options}\n\n输入选项 (online/workshop/external/conference/mentor):`);
    
    if (!choice || !TRAINING_TYPES[choice]) {
        return;
    }
    
    const selected = TRAINING_TYPES[choice];
    
    if (!confirm(`确认培训:\n\n类型：${selected.name}\n时长：${selected.days}天\n成本：$${selected.cost.toLocaleString()}\n技能点：+${selected.points}\n\n确定吗？`)) {
        return;
    }
    
    try {
        const result = await api.trainAgent(agentId, choice);
        if (result.success) {
            const r = result.result;
            showNotification(`✅ 培训完成！\n${selected.name}: +${r.skill_points_gained}技能点\n总技能点：${r.total_skill_points}\n${r.leveled_up ? '🎉 升级了！' : ''}`, 'success');
            updateAgentsList();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error || '培训失败'}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
};

// 切换标签
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    const tab = document.getElementById(`tab-${tabName}`);
    if (tab) {
        tab.classList.add('active');
        if (tabName === 'agents') updateAgentsList();
        else if (tabName === 'projects') updateProjectsList();
        else if (tabName === 'bond') updateBondPanel();
        else if (tabName === 'equipment') updateEquipmentPanel();
        else if (tabName === 'brand') updateBrandPanel();
        else if (tabName === 'funding') updateFundingPanel();
    }
}

// 更新 UI
function updateUI(status) {
    if (!status) return;
    gameState = status;
    
    document.getElementById('cash').textContent = `$${(status.cash || 0).toLocaleString()}`;
    document.getElementById('reputation').textContent = `${status.reputation || 3.0}/5.0`;
    document.getElementById('day').textContent = status.day || 0;
    document.getElementById('agents').textContent = `${status.agent_count || 0}/${status.max_agents || 5}`;
    
    const expenses = status.daily_expenses || 0;
    document.getElementById('daily-salary').textContent = `-$${(expenses * 0.7).toLocaleString()}`;
    document.getElementById('daily-rent').textContent = `-$${(expenses * 0.3).toLocaleString()}`;
    document.getElementById('daily-expenses').textContent = `-$${expenses.toLocaleString()}`;
    
    updateAgentsList();
    updateProjectsList();
}

// 更新羁绊面板
async function updateBondPanel() {
    try {
        const bond = await api.getBondStatus();
        if (!bond || bond.error) return;
        
        document.getElementById('bond-tier').textContent = bond.name;
        document.getElementById('bond-days').textContent = `${bond.bond_days} 天`;
        document.getElementById('bond-bonus').textContent = `+${(bond.quality_bonus * 100).toFixed(0)}%`;
        
        if (bond.next_tier !== null) {
            const tierNames = {0: "陌生", 1: "相识", 2: "默契", 3: "信赖", 4: "灵魂伴侣"};
            document.getElementById('bond-next').textContent = `${tierNames[bond.next_tier]} (${bond.days_to_next}天)`;
            
            // 计算进度百分比
            const currentMin = bond.bond_days - bond.days_to_next + (bond.next_tier === 1 ? 8 : bond.next_tier === 2 ? 23 : bond.next_tier === 3 ? 30 : 39);
            const progress = Math.min(100, (bond.bond_days / (bond.next_tier === 1 ? 8 : bond.next_tier === 2 ? 31 : bond.next_tier === 3 ? 61 : 100)) * 100);
            document.getElementById('bond-progress').style.width = `${progress}%`;
            document.getElementById('bond-progress-text').textContent = `${progress.toFixed(0)}%`;
        } else {
            document.getElementById('bond-next').textContent = "已满级";
            document.getElementById('bond-progress').style.width = "100%";
            document.getElementById('bond-progress-text').textContent = "100%";
        }
    } catch (e) {
        console.error('更新羁绊面板失败:', e);
    }
}

// 更新员工列表
async function updateAgentsList() {
    try {
        const result = await api.listAgents();
        const container = document.getElementById('agents-list');
        
        if (!result.agents || result.agents.length === 0) {
            container.innerHTML = '<p>暂无员工</p>';
            return;
        }
        
        container.innerHTML = result.agents.map((agent, index) => `
            <div class="card">
                <div class="card-header">
                    <span>👨‍💻 ${agent.name} (Lv${agent.level})</span>
                    <div style="float:right;">
                        <button class="btn btn-primary btn-sm" onclick="trainAgent('${agent.id}', '${agent.name}')" style="float:right;padding:2px 8px;font-size:12px;margin-right:5px;">📚 培训</button>
                        <button class="btn btn-danger btn-sm" onclick="fireAgent('${agent.id}', '${agent.name}')" style="float:right;padding:2px 8px;font-size:12px;">解雇</button>
                    </div>
                </div>
                <div class="card-body">
                    <div class="card-row"><span class="card-label">职位:</span><span class="card-value">${agent.role}</span></div>
                    <div class="card-row"><span class="card-label">效率:</span><span class="card-value">${agent.efficiency}</span></div>
                    <div class="card-row"><span class="card-label">协作:</span><span class="card-value">${agent.collaboration || 50}</span></div>
                    <div class="card-row"><span class="card-label">技能点:</span><span class="card-value">${agent.skill_points || 0} (升级需 100)</span></div>
                    <div class="card-row"><span class="card-label">羁绊:</span><span class="card-value">${agent.bond_days || 0}天</span></div>
                    <div class="card-row"><span class="card-label">薪资:</span><span class="card-value">$${agent.salary.toLocaleString()}/天</span></div>
                </div>
            </div>
        `).join('');
    } catch (e) {
        console.error('更新员工失败:', e);
    }
}

// 更新项目列表
async function updateProjectsList() {
    try {
        const result = await api.listProjects();
        const container = document.getElementById('projects-list');
        
        if (!result.projects || result.projects.length === 0) {
            container.innerHTML = '<p>暂无项目</p>';
            return;
        }
        
        container.innerHTML = result.projects.map(project => {
            const progress = project.progress || 0;
            const emoji = {'available': '📋', 'in_progress': '⚙️', 'completed': '✅', 'failed': '❌'}[project.status] || '📋';
            
            return `
                <div class="card">
                    <div class="card-header">${emoji} ${project.name}</div>
                    <div class="card-body">
                        <div class="card-row"><span class="card-label">类型:</span><span class="card-value">${project.type}</span></div>
                        <div class="card-row"><span class="card-label">报酬:</span><span class="card-value">$${project.reward.toLocaleString()}</span></div>
                        <div class="card-row"><span class="card-label">截止:</span><span class="card-value">${project.days_remaining}天</span></div>
                        <div class="progress-bar"><div class="progress-fill" style="width: ${progress}%"></div></div>
                        <div class="card-row"><span class="card-label">进度:</span><span class="card-value">${progress}%</span></div>
                    </div>
                    ${project.status === 'available' ? `<button class="btn btn-success" onclick="acceptProject('${project.id}')">接受</button>` : ''}
                    ${project.status === 'in_progress' && progress >= 100 ? `<button class="btn btn-primary" onclick="completeProject('${project.id}')">交付</button>` : ''}
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('更新项目失败:', e);
    }
}

// 接受项目
async function acceptProject(projectId) {
    try {
        const result = await api.acceptProject(projectId);
        if (result.success) {
            showNotification('✅ 已接受', 'success');
            updateProjectsList();
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

// 完成项目
async function completeProject(projectId) {
    try {
        const result = await api.completeProject(projectId);
        if (result.success) {
            showNotification(`✅ 获得 $${result.reward.toLocaleString()}`, 'success');
            updateProjectsList();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

// 显示通知
function showNotification(message, type = 'info') {
    const container = document.getElementById('notifications');
    const div = document.createElement('div');
    div.className = `notification ${type}`;
    div.textContent = message;
    container.appendChild(div);
    setTimeout(() => div.remove(), 5000);
}

// ========== Phase 3.3: 设备中心 ==========

async function updateEquipmentPanel() {
    try {
        const data = await api.getEquipments();
        const container = document.getElementById('equipment-list');
        const owned = data.equipments || [];
        const config = data.config || {};
        
        const equipmentIcons = {
            '高速网络': '🌐',
            '开发者工作站': '💻',
            '云服务器集群': '☁️',
            '测试实验室': '🔬',
            'AI 训练集群': '🤖',
        };
        
        container.innerHTML = Object.entries(config).map(([name, cfg]) => {
            const isOwned = owned.includes(name);
            const icon = equipmentIcons[name] || '🔧';
            const officeReq = cfg.office_required || 1;
            const bonus = cfg.bonus || 0;
            
            return `
                <div class="card" style="${isOwned ? 'opacity:0.6;' : ''}">
                    <div class="card-header">${icon} ${name} ${isOwned ? '✅' : ''}</div>
                    <div class="card-body">
                        <div class="card-row"><span class="card-label">价格:</span><span class="card-value">$${cfg.cost.toLocaleString()}</span></div>
                        <div class="card-row"><span class="card-label">加成:</span><span class="card-value">+${(bonus * 100).toFixed(0)}%</span></div>
                        <div class="card-row"><span class="card-label">解锁条件:</span><span class="card-value">办公室 ≥ Lv.${officeReq}</span></div>
                        ${!isOwned ? `<button class="btn btn-success" onclick="buyEquipment('${name}')">购买</button>` : '<p style="color:#28a745;">已购买</p>'}
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('更新设备面板失败:', e);
    }
}

async function buyEquipment(name) {
    try {
        const result = await api.buyEquipment(name);
        if (result.success) {
            showNotification(`✅ 购买了 ${name}`, 'success');
            updateEquipmentPanel();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

// ========== Phase 3.3: 品牌管理 ==========

async function updateBrandPanel() {
    try {
        const brand = await api.getBrandStatus();
        document.getElementById('brand-level').textContent = brand.brand_name || '无名小卒';
        document.getElementById('brand-mult').textContent = `${(brand.multiplier || 1.0).toFixed(1)}x`;
        document.getElementById('brand-cost').textContent = `$${(brand.daily_cost || 0).toLocaleString()}`;
        
        const container = document.getElementById('marketing-list');
        const config = brand.marketing_config || {};
        
        const campaignIcons = {
            '社交媒体推广': '📱',
            '行业展会参展': '🎪',
            '电视广告': '📺',
            '全球发布会': '🌍',
        };
        
        container.innerHTML = Object.entries(config).map(([name, cfg]) => {
            const icon = campaignIcons[name] || '📢';
            return `
                <div class="card">
                    <div class="card-header">${icon} ${name}</div>
                    <div class="card-body">
                        <div class="card-row"><span class="card-label">成本:</span><span class="card-value">$${cfg.cost.toLocaleString()}</span></div>
                        <div class="card-row"><span class="card-label">品牌提升:</span><span class="card-value">+${cfg.level_up} 级</span></div>
                        <button class="btn btn-success" onclick="runMarketing('${name}')">执行</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('更新品牌面板失败:', e);
    }
}

async function runMarketing(name) {
    try {
        const result = await api.runMarketing(name);
        if (result.success) {
            showNotification(`✅ 品牌升级到 Lv.${result.brand_level}`, 'success');
            updateBrandPanel();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

// ========== Phase 3.3: 融资中心 ==========

async function updateFundingPanel() {
    try {
        const funding = await api.getFundingStatus();
        document.getElementById('equity-sold').textContent = `${(funding.equity_sold * 100).toFixed(0)}%`;
        document.getElementById('dividend-rate').textContent = `${(funding.dividend_rate * 100).toFixed(0)}%`;
        document.getElementById('founder-out').textContent = funding.founder_out ? '⚠️ 是' : '否';
        document.getElementById('founder-out').style.color = funding.founder_out ? '#dc3545' : '#28a745';
        
        const container = document.getElementById('funding-rounds');
        const config = funding.funding_config || {};
        const status = await api.getGameStatus();
        
        const roundIcons = {
            '种子轮': '🌱',
            '天使轮': '👼',
            'A 轮': '🅰️',
            'B 轮': '🅱️',
            'IPO': '📈',
        };
        
        container.innerHTML = Object.entries(config).map(([name, cfg]) => {
            const icon = roundIcons[name] || '💰';
            const canApply = status.day >= cfg.min_day && status.reputation >= cfg.min_reputation;
            const alreadyFunded = funding.investors && funding.investors.some(i => i.round === name);
            
            return `
                <div class="card" style="${alreadyFunded ? 'opacity:0.6;' : ''}">
                    <div class="card-header">${icon} ${name} ${alreadyFunded ? '✅' : ''}</div>
                    <div class="card-body">
                        <div class="card-row"><span class="card-label">融资金额:</span><span class="card-value">$${cfg.amount.toLocaleString()}</span></div>
                        <div class="card-row"><span class="card-label">出让股权:</span><span class="card-value">${(cfg.equity * 100).toFixed(0)}%</span></div>
                        <div class="card-row"><span class="card-label">季度分红:</span><span class="card-value">${(cfg.dividend_rate * 100).toFixed(0)}%</span></div>
                        <div class="card-row"><span class="card-label">解锁条件:</span><span class="card-value">第 ${cfg.min_day} 天, reputation ≥ ${cfg.min_reputation}</span></div>
                        ${!alreadyFunded ? (canApply ? `<button class="btn btn-success" onclick="applyFunding('${name}')">申请融资</button>` : '<button class="btn btn-secondary" disabled>未解锁</button>') : '<p style="color:#28a745;">已融资</p>'}
                    </div>
                </div>
            `;
        }).join('');
    } catch (e) {
        console.error('更新融资面板失败:', e);
    }
}

async function applyFunding(name) {
    try {
        const result = await api.applyFunding(name);
        if (result.success) {
            showNotification(`✅ ${name}融资成功! 现金 +$${result.cash.toLocaleString()}`, 'success');
            updateFundingPanel();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

async function buybackEquity() {
    const amount = parseFloat(document.getElementById('buyback-amount').value);
    if (!amount || amount <= 0) {
        showNotification('❌ 请输入有效金额', 'error');
        return;
    }
    
    try {
        const result = await api.buybackEquity(amount);
        if (result.success) {
            showNotification(`✅ 回购成功! 回购 ${((result.equity_bought || 0) * 100).toFixed(1)}% 股权`, 'success');
            updateFundingPanel();
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification(`❌ ${result.error}`, 'error');
        }
    } catch (e) {
        showNotification(`❌ ${e.message}`, 'error');
    }
}

// 导出全局函数
window.nextDay = nextDay;
window.newGame = newGame;
window.upgradeOffice = upgradeOffice;
window.hireAgent = hireAgent;
window.showTab = showTab;
window.acceptProject = acceptProject;
window.completeProject = completeProject;
window.updateBondPanel = updateBondPanel;
window.buyEquipment = buyEquipment;
window.runMarketing = runMarketing;
window.maintainBrand = maintainBrand;
window.applyFunding = applyFunding;
window.buybackEquity = buybackEquity;

// ========== 成就系统 ==========

let allAchievements = [];
let currentCategory = 'all';
let currentStatus = 'all';

// 加载成就列表
async function loadAchievements() {
    try {
        const response = await fetch('/api/achievements');
        const data = await response.json();
        allAchievements = data.achievements || [];
        
        // 更新概览
        document.getElementById('ach-unlocked-count').textContent = data.unlocked_count || 0;
        document.getElementById('ach-total-count').textContent = data.total_count || 52;
        const rate = data.total_count > 0 ? Math.round((data.unlocked_count / data.total_count) * 100) : 0;
        document.getElementById('ach-rate').textContent = rate + '%';
        document.getElementById('ach-progress-text').textContent = `${data.unlocked_count || 0} / ${data.total_count || 52}`;
        document.getElementById('ach-progress-fill').style.width = rate + '%';
        
        renderAchievements();
    } catch (e) {
        console.error('加载成就失败:', e);
    }
}

// 渲染成就列表
function renderAchievements() {
    const container = document.getElementById('achievement-list');
    const emptyState = document.getElementById('achievement-empty');
    
    let filtered = allAchievements.filter(a => {
        // 分类筛选
        if (currentCategory !== 'all' && a.category !== currentCategory) return false;
        // 状态筛选
        if (currentStatus === 'unlocked' && !a.unlocked) return false;
        if (currentStatus === 'locked' && a.unlocked) return false;
        return true;
    });
    
    if (filtered.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    container.innerHTML = filtered.map(a => renderAchievementCard(a)).join('');
}

// 渲染单个成就卡片
function renderAchievementCard(a) {
    const isHidden = a.category === '隐藏';
    
    if (a.unlocked) {
        return `
            <div class="achievement-card unlocked" data-category="${a.category}" data-id="${a.id}">
                <div class="achievement-icon">${a.icon}</div>
                <div class="achievement-info">
                    <div class="achievement-name">${a.name}</div>
                    <div class="achievement-desc">${a.description}</div>
                    <div class="achievement-meta">
                        <span class="achievement-category">${getCategoryIcon(a.category)} ${a.category}</span>
                    </div>
                </div>
                <div class="achievement-badge">✅</div>
            </div>
        `;
    } else {
        const name = isHidden ? '???' : a.name;
        const desc = isHidden ? '这是一个秘密...' : a.description;
        const icon = isHidden ? '❓' : '🔒';
        
        return `
            <div class="achievement-card locked ${isHidden ? 'hidden-achievement' : ''}" data-category="${a.category}" data-id="${a.id}">
                <div class="achievement-icon locked-icon">${icon}</div>
                <div class="achievement-info">
                    <div class="achievement-name locked-name">${name}</div>
                    <div class="achievement-desc locked-desc">${desc}</div>
                </div>
                <div class="achievement-badge locked-badge">${isHidden ? '❓' : '🔒'}</div>
            </div>
        `;
    }
}

// 获取分类图标
function getCategoryIcon(category) {
    const icons = {
        '成长': '🎯',
        '项目': '💎',
        '团队': '👥',
        '设备': '🔧',
        '品牌': '🏷️',
        '融资': '💹',
        '财务': '💰',
        '隐藏': '❓'
    };
    return icons[category] || '🏆';
}

// 分类筛选
function filterAchievements(category, btn) {
    currentCategory = category;
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderAchievements();
}

// 状态筛选
function filterStatus(status, btn) {
    currentStatus = status;
    document.querySelectorAll('.status-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderAchievements();
}

// 成就解锁弹窗
function showAchievementPopup(achievement) {
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="popup-title">🏆 成就解锁！</div>
        <div class="popup-name">${achievement.icon} ${achievement.name}</div>
        <div class="popup-desc">${achievement.description}</div>
    `;
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 4000);
}

// 检查新成就
async function checkAchievements() {
    try {
        const response = await fetch('/api/achievements/check', { method: 'POST' });
        const data = await response.json();
        
        if (data.new_unlocks && data.new_unlocks.length > 0) {
            data.new_unlocks.forEach(aid => {
                const achievement = allAchievements.find(a => a.id === aid);
                if (achievement) {
                    showAchievementPopup(achievement);
                    achievement.unlocked = true;
                }
            });
            // 更新概览
            const total = allAchievements.length;
            document.getElementById('ach-unlocked-count').textContent = data.total_unlocked;
            const rate = Math.round((data.total_unlocked / total) * 100);
            document.getElementById('ach-rate').textContent = rate + '%';
            document.getElementById('ach-progress-text').textContent = `${data.total_unlocked} / ${total}`;
            document.getElementById('ach-progress-fill').style.width = rate + '%';
            renderAchievements();
        }
    } catch (e) {
        console.error('检查成就失败:', e);
    }
}

// 扩展 showTab 以支持成就标签页
const _origShowTab = window.showTab;
window.showTab = function(tabName) {
    if (_origShowTab) _origShowTab(tabName);
    if (tabName === 'achievements') {
        loadAchievements();
    }
};

// 导出全局函数
window.loadAchievements = loadAchievements;
window.renderAchievements = renderAchievements;
window.filterAchievements = filterAchievements;
window.filterStatus = filterStatus;
window.showAchievementPopup = showAchievementPopup;
window.checkAchievements = checkAchievements;
