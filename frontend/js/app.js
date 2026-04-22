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
    try {
        const result = await api.upgradeOffice();
        if (result.success) {
            showNotification(`✅ 升级到 Lv${result.office_level}！`, 'success');
            const status = await api.getGameStatus();
            updateUI(status);
        } else {
            showNotification('❌ 资金不足', 'error');
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

// 切换标签
function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    const tab = document.getElementById(`tab-${tabName}`);
    if (tab) {
        tab.classList.add('active');
        if (tabName === 'agents') updateAgentsList();
        else if (tabName === 'projects') updateProjectsList();
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

// 更新员工列表
async function updateAgentsList() {
    try {
        const result = await api.listAgents();
        const container = document.getElementById('agents-list');
        
        if (!result.agents || result.agents.length === 0) {
            container.innerHTML = '<p>暂无员工</p>';
            return;
        }
        
        container.innerHTML = result.agents.map(agent => `
            <div class="card">
                <div class="card-header">👨‍💻 ${agent.name}</div>
                <div class="card-body">
                    <div class="card-row"><span class="card-label">职位:</span><span class="card-value">${agent.role}</span></div>
                    <div class="card-row"><span class="card-label">等级:</span><span class="card-value">Lv${agent.level}</span></div>
                    <div class="card-row"><span class="card-label">效率:</span><span class="card-value">${agent.efficiency}</span></div>
                    <div class="card-row"><span class="card-label">满意度:</span><span class="card-value">${agent.satisfaction}%</span></div>
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

// 导出全局函数
window.nextDay = nextDay;
window.newGame = newGame;
window.upgradeOffice = upgradeOffice;
window.hireAgent = hireAgent;
window.showTab = showTab;
window.acceptProject = acceptProject;
window.completeProject = completeProject;
