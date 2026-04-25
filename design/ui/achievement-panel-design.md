# 成就系统 UI 面板设计

**版本**: v1.0  
**日期**: 2026-04-25  
**创意总监**: 创意总监  
**用途**: 全栈开发直接落前端的完整设计稿

---

## 1. 后端 API 现状（已实现，commit 9140b50）

### API 路由（`backend/routes/achievement_routes.py`）

| API | 方法 | 路径 | 返回 |
|-----|------|------|------|
| 全部成就 | GET | `/api/achievements` | `{achievements: [...], unlocked_count, total_count}` |
| 已解锁 | GET | `/api/achievements/unlocked` | `{achievements: [...]}` |
| 成就进度 | GET | `/api/achievements/progress/<id>` | `{id, name, icon, unlocked, progress: 0-100}` |
| 检查成就 | POST | `/api/achievements/check` | `{new_unlocks: [...], total_unlocked}` |

### 成就数据模型（`backend/services/achievement_engine.py`）

**52 个成就，8 个分类**：

| 分类 | 数量 | 图标前缀 |
|------|------|---------|
| 成长 | 10 | 🎯🌱🌿🔥📅⏳🏠⭐🏆🎂 |
| 项目 | 8 | 💎⚡🚨🎨💰🎯💀🔄 |
| 团队 | 7 | 👤👥🏢🎓🧙🛡️😈 |
| 设备 | 4 | 🌐🏆💰🤖 |
| 品牌 | 5 | 🌒🌓🌔🌕🌟 |
| 融资 | 7 | 🌱👼🅰️🅱️📈👑⚠️ |
| 财务 | 5 | 💵💎🏦📊🤑 |
| 隐藏 | 6 | ⚡📉💔🏃🔧🎪 |

### Company 数据模型（`backend/models/company.py` 第 87-88 行）

```python
achievements: List[str] = field(default_factory=list)       # 已解锁成就 ID 列表
achievement_progress: Dict[str, dict] = field(default_factory=dict)  # 进度记录
```

---

## 2. index.html 修改

### 2.1 操作面板新增按钮

在 `💰 融资中心` 按钮之后添加：

```html
<button class="btn btn-warning" onclick="showTab('achievements')">🏆 成就</button>
```

### 2.2 新增标签页内容

在 `tab-funding` 的 `</div>` 之后插入：

```html
<!-- 成就面板 -->
<div id="tab-achievements" class="tab-content">
    <h2>🏆 成就系统</h2>
    <p class="tab-desc">完成挑战解锁成就，展示你的创业历程。</p>

    <!-- 成就概览 -->
    <div class="achievement-overview">
        <div class="overview-stat achievement-stat">
            <span class="stat-icon">🏆</span>
            <span class="stat-number" id="ach-unlocked-count">0</span>
            <span class="stat-label">已解锁</span>
        </div>
        <div class="overview-stat achievement-stat">
            <span class="stat-icon">📊</span>
            <span class="stat-number" id="ach-total-count">52</span>
            <span class="stat-label">总成就</span>
        </div>
        <div class="overview-stat achievement-stat">
            <span class="stat-icon">📈</span>
            <span class="stat-number" id="ach-rate">0%</span>
            <span class="stat-label">解锁率</span>
        </div>
    </div>

    <!-- 成就进度条 -->
    <div class="achievement-progress-bar">
        <div class="progress-label">
            <span>总进度</span>
            <span id="ach-progress-text">0 / 52</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="ach-progress-fill" style="width: 0%"></div>
        </div>
    </div>

    <!-- 分类筛选 -->
    <div class="achievement-filters">
        <button class="filter-btn active" data-category="all" onclick="filterAchievements('all', this)">全部</button>
        <button class="filter-btn" data-category="成长" onclick="filterAchievements('成长', this)">🎯 成长</button>
        <button class="filter-btn" data-category="项目" onclick="filterAchievements('项目', this)">💎 项目</button>
        <button class="filter-btn" data-category="团队" onclick="filterAchievements('团队', this)">👥 团队</button>
        <button class="filter-btn" data-category="设备" onclick="filterAchievements('设备', this)">🔧 设备</button>
        <button class="filter-btn" data-category="品牌" onclick="filterAchievements('品牌', this)">🏷️ 品牌</button>
        <button class="filter-btn" data-category="融资" onclick="filterAchievements('融资', this)">💹 融资</button>
        <button class="filter-btn" data-category="财务" onclick="filterAchievements('财务', this)">💰 财务</button>
        <button class="filter-btn" data-category="隐藏" onclick="filterAchievements('隐藏', this)">❓ 隐藏</button>
    </div>

    <!-- 显示筛选：全部/已解锁/未解锁 -->
    <div class="achievement-status-filters">
        <button class="status-btn active" data-status="all" onclick="filterStatus('all', this)">全部</button>
        <button class="status-btn" data-status="unlocked" onclick="filterStatus('unlocked', this)">✅ 已解锁</button>
        <button class="status-btn" data-status="locked" onclick="filterStatus('locked', this)">🔒 未解锁</button>
    </div>

    <!-- 成就列表 -->
    <div id="achievement-list" class="achievement-grid">
        <!-- 动态渲染 -->
    </div>

    <!-- 空状态 -->
    <div id="achievement-empty" class="empty-state" style="display:none;">
        <div class="empty-icon">🏆</div>
        <p>还没有解锁任何成就</p>
        <p class="empty-hint">继续游戏，完成挑战来解锁成就！</p>
    </div>
</div>
```

---

## 3. 成就卡片设计

### 已解锁成就卡片

```html
<div class="achievement-card unlocked" data-category="成长" data-id="first_project">
    <div class="achievement-icon">🎯</div>
    <div class="achievement-info">
        <div class="achievement-name">迈出第一步</div>
        <div class="achievement-desc">完成了第一个项目</div>
        <div class="achievement-meta">
            <span class="achievement-category">🎯 成长</span>
            <span class="achievement-time">📅 第 3 天解锁</span>
        </div>
    </div>
    <div class="achievement-badge">✅</div>
</div>
```

### 未解锁成就卡片

```html
<div class="achievement-card locked" data-category="项目" data-id="perfect_quality">
    <div class="achievement-icon locked-icon">🔒</div>
    <div class="achievement-info">
        <div class="achievement-name locked-name">???</div>
        <div class="achievement-desc locked-desc">完成一次质量 100 的项目</div>
        <div class="achievement-progress">
            <div class="progress-bar">
                <div class="progress-fill" style="width: 45%"></div>
            </div>
            <span class="progress-percent">45%</span>
        </div>
    </div>
    <div class="achievement-badge locked-badge">🔒</div>
</div>
```

### 隐藏成就卡片（未解锁时）

```html
<div class="achievement-card locked hidden-achievement" data-category="隐藏" data-id="speed_demon_2">
    <div class="achievement-icon locked-icon">❓</div>
    <div class="achievement-info">
        <div class="achievement-name locked-name">???</div>
        <div class="achievement-desc locked-desc">这是一个秘密...</div>
    </div>
    <div class="achievement-badge locked-badge">❓</div>
</div>
```

### 卡片视觉状态

| 状态 | 卡片背景 | 边框 | 图标 | 名称 |
|------|---------|------|------|------|
| 已解锁 | `#fff` 白底 | `#2ecc71` 绿 | 显示真实 emoji | 正常显示 |
| 未解锁 | `#f8f9fa` 浅灰 | `#dee2e6` 灰 | 🔒 锁图标 | `???` |
| 隐藏（未解锁） | `#f0f0f0` 更浅灰 | `#e0e0e0` 浅灰 | ❓ 问号 | `???` |
| 悬停 | `#f0f7ff` 浅蓝 | `#3498db` 蓝 | — | — |

---

## 4. CSS 新增样式

追加到 `frontend/css/style.css`：

```css
/* ========== 成就面板 ========== */

/* 成就概览 */
.achievement-overview {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}

.achievement-stat {
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    color: white;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
}

.achievement-stat .stat-icon { font-size: 1.8em; }
.achievement-stat .stat-number { font-size: 1.5em; font-weight: bold; }
.achievement-stat .stat-label { font-size: 0.85em; opacity: 0.9; }

/* 成就进度条 */
.achievement-progress-bar {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 12px 15px;
    margin-bottom: 20px;
}

.achievement-progress-bar .progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.9em;
    color: #666;
    margin-bottom: 8px;
}

.achievement-progress-bar .progress-fill {
    background: linear-gradient(90deg, #f39c12, #e67e22);
}

/* 分类筛选 */
.achievement-filters {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 12px;
}

.filter-btn {
    padding: 6px 14px;
    border: 2px solid #dee2e6;
    border-radius: 20px;
    background: white;
    font-size: 0.85em;
    cursor: pointer;
    transition: all 0.2s;
    color: #666;
}

.filter-btn:hover {
    border-color: #3498db;
    color: #3498db;
}

.filter-btn.active {
    background: #3498db;
    border-color: #3498db;
    color: white;
}

/* 状态筛选 */
.achievement-status-filters {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}

.status-btn {
    padding: 6px 14px;
    border: 2px solid #dee2e6;
    border-radius: 20px;
    background: white;
    font-size: 0.85em;
    cursor: pointer;
    transition: all 0.2s;
    color: #666;
}

.status-btn:hover {
    border-color: #2ecc71;
    color: #2ecc71;
}

.status-btn.active {
    background: #2ecc71;
    border-color: #2ecc71;
    color: white;
}

/* 成就网格 */
.achievement-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 12px;
}

/* 成就卡片 */
.achievement-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px;
    background: white;
    border-radius: 10px;
    border: 2px solid #dee2e6;
    transition: all 0.3s;
}

.achievement-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 已解锁 */
.achievement-card.unlocked {
    border-color: #2ecc71;
    background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
}

.achievement-card.unlocked .achievement-icon {
    font-size: 2.2em;
    animation: achievementGlow 2s ease-in-out infinite;
}

@keyframes achievementGlow {
    0%, 100% { filter: drop-shadow(0 0 3px rgba(46, 204, 113, 0.3)); }
    50% { filter: drop-shadow(0 0 8px rgba(46, 204, 113, 0.6)); }
}

/* 未解锁 */
.achievement-card.locked {
    background: #f8f9fa;
    opacity: 0.85;
}

.achievement-card.locked .locked-icon {
    font-size: 1.8em;
    opacity: 0.4;
}

.achievement-card.locked .locked-name {
    color: #999;
    font-style: italic;
}

.achievement-card.locked .locked-desc {
    color: #bbb;
}

/* 隐藏成就 */
.achievement-card.hidden-achievement {
    background: #f0f0f0;
    border-color: #e0e0e0;
}

/* 成就图标 */
.achievement-icon {
    font-size: 2.2em;
    min-width: 50px;
    text-align: center;
}

/* 成就信息 */
.achievement-info {
    flex: 1;
    min-width: 0;
}

.achievement-name {
    font-size: 1em;
    font-weight: bold;
    color: #333;
    margin-bottom: 4px;
}

.achievement-desc {
    font-size: 0.85em;
    color: #666;
    margin-bottom: 6px;
}

.achievement-meta {
    display: flex;
    gap: 12px;
    font-size: 0.75em;
    color: #999;
}

.achievement-category {
    background: #f0f0f0;
    padding: 2px 8px;
    border-radius: 10px;
}

.achievement-time {
    color: #2ecc71;
}

/* 成就进度（未解锁时显示） */
.achievement-progress {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 6px;
}

.achievement-progress .progress-bar {
    flex: 1;
    height: 8px;
    margin: 0;
}

.achievement-progress .progress-fill {
    background: linear-gradient(90deg, #3498db, #2ecc71);
}

.progress-percent {
    font-size: 0.8em;
    color: #666;
    min-width: 35px;
    text-align: right;
}

/* 成就徽章 */
.achievement-badge {
    font-size: 1.5em;
    min-width: 30px;
    text-align: center;
}

.locked-badge {
    opacity: 0.3;
}

/* 成就解锁弹窗 */
.achievement-popup {
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
    color: white;
    padding: 20px 25px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(243, 156, 18, 0.4);
    z-index: 2000;
    animation: slideInRight 0.5s ease-out, slideOutRight 0.5s ease-in 3.5s forwards;
    max-width: 350px;
}

.achievement-popup .popup-icon {
    font-size: 2em;
    margin-right: 12px;
    vertical-align: middle;
}

.achievement-popup .popup-title {
    font-size: 0.85em;
    opacity: 0.9;
    margin-bottom: 4px;
}

.achievement-popup .popup-name {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 4px;
}

.achievement-popup .popup-desc {
    font-size: 0.9em;
    opacity: 0.85;
}

@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOutRight {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}

/* 排行榜 */
.leaderboard-section {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 2px solid #eee;
}

.leaderboard-section h3 {
    margin-bottom: 15px;
    color: #333;
}

.leaderboard-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
}

.leaderboard-tab {
    padding: 8px 16px;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    background: white;
    font-size: 0.9em;
    cursor: pointer;
    transition: all 0.2s;
}

.leaderboard-tab.active {
    background: #667eea;
    border-color: #667eea;
    color: white;
}

.leaderboard-list {
    background: #f8f9fa;
    border-radius: 10px;
    overflow: hidden;
}

.leaderboard-item {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
    transition: background 0.2s;
}

.leaderboard-item:last-child {
    border-bottom: none;
}

.leaderboard-item:hover {
    background: #f0f7ff;
}

.leaderboard-rank {
    font-size: 1.2em;
    font-weight: bold;
    min-width: 40px;
    text-align: center;
}

.leaderboard-rank.gold { color: #f39c12; }
.leaderboard-rank.silver { color: #95a5a6; }
.leaderboard-rank.bronze { color: #cd7f32; }

.leaderboard-avatar {
    font-size: 1.5em;
    margin: 0 12px;
}

.leaderboard-info {
    flex: 1;
}

.leaderboard-name {
    font-weight: bold;
    color: #333;
}

.leaderboard-stats {
    font-size: 0.85em;
    color: #666;
}

.leaderboard-score {
    font-size: 1.1em;
    font-weight: bold;
    color: #667eea;
}

/* 响应式 */
@media (max-width: 768px) {
    .achievement-overview { grid-template-columns: 1fr; }
    .achievement-grid { grid-template-columns: 1fr; }
    .achievement-filters { gap: 6px; }
    .filter-btn, .status-btn { font-size: 0.8em; padding: 5px 10px; }
}
```

---

## 5. JavaScript 逻辑

追加到 `frontend/js/app.js`：

```javascript
// ========== 成就系统 ==========

let allAchievements = [];
let currentCategory = 'all';
let currentStatus = 'all';

// 加载成就列表
async function loadAchievements() {
    try {
        const response = await fetch('/api/achievements');
        const data = await response.json();
        
        if (data.error) return;
        
        allAchievements = data.achievements;
        
        // 更新概览
        document.getElementById('ach-unlocked-count').textContent = data.unlocked_count;
        document.getElementById('ach-total-count').textContent = data.total_count;
        document.getElementById('ach-rate').textContent = 
            Math.round((data.unlocked_count / data.total_count) * 100) + '%';
        document.getElementById('ach-progress-text').textContent = 
            `${data.unlocked_count} / ${data.total_count}`;
        document.getElementById('ach-progress-fill').style.width = 
            ((data.unlocked_count / data.total_count) * 100) + '%';
        
        renderAchievements();
        
    } catch (e) {
        console.error('加载成就失败:', e);
    }
}

// 渲染成就列表
function renderAchievements() {
    const container = document.getElementById('achievement-list');
    const emptyState = document.getElementById('achievement-empty');
    
    let filtered = allAchievements;
    
    // 分类筛选
    if (currentCategory !== 'all') {
        filtered = filtered.filter(a => a.category === currentCategory);
    }
    
    // 状态筛选
    if (currentStatus === 'unlocked') {
        filtered = filtered.filter(a => a.unlocked);
    } else if (currentStatus === 'locked') {
        filtered = filtered.filter(a => !a.unlocked);
    }
    
    if (filtered.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    // 按分类分组
    const grouped = {};
    filtered.forEach(a => {
        if (!grouped[a.category]) grouped[a.category] = [];
        grouped[a.category].push(a);
    });
    
    let html = '';
    const categoryIcons = {
        '成长': '🎯', '项目': '💎', '团队': '👥', '设备': '🔧',
        '品牌': '🏷️', '融资': '💹', '财务': '💰', '隐藏': '❓'
    };
    
    for (const [category, achievements] of Object.entries(grouped)) {
        html += `<div class="achievement-category-group">
            <h3 class="category-title">${categoryIcons[category] || '📋'} ${category} (${achievements.filter(a => a.unlocked).length}/${achievements.length})</h3>
            <div class="achievement-grid">`;
        
        achievements.forEach(a => {
            if (a.unlocked) {
                html += renderUnlockedAchievement(a);
            } else {
                html += renderLockedAchievement(a);
            }
        });
        
        html += '</div></div>';
    }
    
    container.innerHTML = html;
}

// 渲染已解锁成就
function renderUnlockedAchievement(a) {
    return `
        <div class="achievement-card unlocked" data-category="${a.category}" data-id="${a.id}">
            <div class="achievement-icon">${a.icon}</div>
            <div class="achievement-info">
                <div class="achievement-name">${a.name}</div>
                <div class="achievement-desc">${a.description}</div>
                <div class="achievement-meta">
                    <span class="achievement-category">${categoryIcons[a.category] || ''} ${a.category}</span>
                </div>
            </div>
            <div class="achievement-badge">✅</div>
        </div>
    `;
}

// 渲染未解锁成就
function renderLockedAchievement(a) {
    const isHidden = a.category === '隐藏';
    const icon = isHidden ? '❓' : '🔒';
    const name = isHidden ? '???' : a.name;
    const desc = isHidden ? '这是一个秘密...' : a.description;
    const cardClass = isHidden ? 'locked hidden-achievement' : 'locked';
    
    return `
        <div class="achievement-card ${cardClass}" data-category="${a.category}" data-id="${a.id}">
            <div class="achievement-icon locked-icon">${icon}</div>
            <div class="achievement-info">
                <div class="achievement-name locked-name">${name}</div>
                <div class="achievement-desc locked-desc">${desc}</div>
            </div>
            <div class="achievement-badge locked-badge">${isHidden ? '❓' : '🔒'}</div>
        </div>
    `;
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

// 检查新成就（在 nextDay 后调用）
async function checkNewAchievements() {
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
            // 更新计数
            document.getElementById('ach-unlocked-count').textContent = data.total_unlocked;
            const total = allAchievements.length;
            document.getElementById('ach-rate').textContent = 
                Math.round((data.total_unlocked / total) * 100) + '%';
            document.getElementById('ach-progress-text').textContent = 
                `${data.total_unlocked} / ${total}`;
            document.getElementById('ach-progress-fill').style.width = 
                ((data.total_unlocked / total) * 100) + '%';
            renderAchievements();
        }
    } catch (e) {
        console.error('检查成就失败:', e);
    }
}

// 扩展 showTab
const _achShowTab = window.showTab;
window.showTab = function(tabName) {
    if (_achShowTab) _achShowTab(tabName);
    if (tabName === 'achievements') {
        loadAchievements();
    }
};

window.loadAchievements = loadAchievements;
window.filterAchievements = filterAchievements;
window.filterStatus = filterStatus;
window.showAchievementPopup = showAchievementPopup;
window.checkNewAchievements = checkNewAchievements;
```

---

## 6. 成就解锁通知文案

### 弹窗标题

```
🏆 成就解锁！
{图标} {成就名称}
{成就描述}
```

### 分类别通知风格

| 分类 | 通知前缀 | 示例 |
|------|---------|------|
| 成长 | `"🎯 成长成就解锁！"` | `"🎯 成长成就解锁！迈出第一步 — 完成了第一个项目"` |
| 项目 | `"💎 项目成就解锁！"` | `"💎 项目成就解锁！完美交付 — 单次项目质量达到 100"` |
| 团队 | `"👥 团队成就解锁！"` | `"👥 团队成就解锁！十人团 — 团队达到 10 人"` |
| 设备 | `"🔧 设备成就解锁！"` | `"🔧 设备成就解锁！装备齐全 — 集齐所有 5 种设备"` |
| 品牌 | `"🏷️ 品牌成就解锁！"` | `"🏷️ 品牌成就解锁！科技帝国 — 品牌达到 Lv5"` |
| 融资 | `"💹 融资成就解锁！"` | `"💹 融资成就解锁！上市敲钟 — 完成 IPO"` |
| 财务 | `"💰 财务成就解锁！"` | `"💰 财务成就解锁！百万俱乐部 — 累计收入达到 $1,000,000"` |
| 隐藏 | `"❓ 隐藏成就解锁！"` | `"❓ 隐藏成就解锁！闪电侠 — 第 1 天就完成项目"` |

---

## 7. 文件修改清单

| 文件 | 操作 | 行数估计 | 内容 |
|------|------|---------|------|
| `frontend/index.html` | 修改 | +2 行 | 新增"成就"按钮 + `tab-achievements` 标签页 |
| `frontend/css/style.css` | 追加 | ~200 行 | 成就面板完整 CSS（含弹窗动画） |
| `frontend/js/app.js` | 追加 | ~150 行 | 成就加载/渲染/筛选/弹窗/检查逻辑 |
| `backend/routes/achievement_routes.py` | 已有 | — | 4 个 API 端点已存在 |
| `backend/services/achievement_engine.py` | 已有 | — | 52 个成就定义 + 检查引擎已存在 |
| `backend/models/company.py` | 已有 | — | `achievements: List[str]` + `achievement_progress` 已存在 |

---

_成就系统 UI 面板设计完毕，后端 API 已就位（commit 9140b50），全栈开发可以直接落前端。_
