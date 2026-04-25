# 羁绊 UI 面板设计

**版本**: v1.0  
**日期**: 2026-04-25  
**创意总监**: 创意总监  
**用途**: 全栈开发直接落前端的完整设计稿

---

## 1. 后端 API 现状（已实现，可直接调用）

### 已有 API 路由

| API | 方法 | 路径 | 返回字段 |
|-----|------|------|---------|
| 双人羁绊 | GET | `/api/company/bond/<emp1_id>/<emp2_id>` | `{emp1, emp2, days, tier, name, quality_bonus, salary_discount, next_tier, days_to_next}` |
| 公司羁绊 | GET | `/api/company/bond-status` | `{tier, name, quality_bonus, bond_days, next_tier, days_to_next}` |
| 员工列表 | GET | `/api/agents` | 含 `bond_days` 字段 |
| 公司状态 | GET | `/api/company` | 含 `bond_pairs: [{emp1, emp2, days}]` |

### PAIR_BOND_TIERS 配置（company.py 第 62-67 行）

| 等级 | 名称 | 所需天数 | 质量加成 | 薪资减免 |
|------|------|---------|---------|---------|
| Lv0 | 陌生人 | 0 天 | 0% | 0% |
| Lv1 | 同事 | 30 天 | +3% | 0% |
| Lv2 | 好友 | 60 天 | +5% | -5% |
| Lv3 | 知己 | 90 天 | +8% | -10% |

### BOND_TIERS 配置（company.py 第 53-58 行）

| 等级 | 名称 | 所需天数 | 质量加成 |
|------|------|---------|---------|
| Lv0 | 陌生 | 0 天 | 0% |
| Lv1 | 相识 | 8 天 | +5% |
| Lv2 | 默契 | 31 天 | +10% |
| Lv3 | 信赖 | 61 天 | +15% |
| Lv4 | 灵魂伴侣 | 100 天 | +20% |

---

## 2. index.html 修改

### 2.1 操作面板新增按钮

在 `🏢 升级办公室` 按钮之后添加：

```html
<button class="btn btn-info" onclick="showTab('bonds')">🤝 团队羁绊</button>
```

### 2.2 新增标签页内容

在 `tab-projects` 的 `</div>` 之后插入：

```html
<!-- 羁绊面板 -->
<div id="tab-bonds" class="tab-content">
    <h2>🤝 团队羁绊</h2>
    <p class="tab-desc">员工在同一项目协作会积累羁绊天数。羁绊等级越高，项目质量加成越大，薪资越低。</p>

    <!-- 概览统计 -->
    <div class="bonds-overview">
        <div class="overview-stat">
            <span class="stat-icon">🤝</span>
            <span class="stat-number" id="bond-pairs-count">0</span>
            <span class="stat-label">活跃羁绊对</span>
        </div>
        <div class="overview-stat">
            <span class="stat-icon">⭐</span>
            <span class="stat-number" id="bond-max-quality">+0%</span>
            <span class="stat-label">最高质量加成</span>
        </div>
        <div class="overview-stat">
            <span class="stat-icon">💰</span>
            <span class="stat-number" id="bond-max-salary">0%</span>
            <span class="stat-label">最高薪资减免</span>
        </div>
    </div>

    <!-- 等级图例 -->
    <div class="bond-legend">
        <span class="legend-item"><span class="level-badge lv0">Lv0</span> 陌生人</span>
        <span class="legend-item"><span class="level-badge lv1">Lv1</span> 同事 (+3%)</span>
        <span class="legend-item"><span class="level-badge lv2">Lv2</span> 好友 (+5%, -5%)</span>
        <span class="legend-item"><span class="level-badge lv3">Lv3</span> 知己 (+8%, -10%)</span>
    </div>

    <!-- 羁绊对列表 -->
    <div id="bond-pairs-list" class="bond-pairs-grid"></div>

    <!-- 空状态 -->
    <div id="bond-empty" class="empty-state" style="display:none;">
        <div class="empty-icon">🤝</div>
        <p>还没有羁绊关系</p>
        <p class="empty-hint">让员工在同一项目协作，羁绊天数会自然增长</p>
    </div>
</div>
```

---

## 3. CSS 新增样式

追加到 `frontend/css/style.css`：

```css
/* ========== 羁绊面板 ========== */

.tab-desc {
    color: #666;
    font-size: 0.95em;
    margin-bottom: 20px;
}

/* 概览统计 */
.bonds-overview {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}

.overview-stat {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
}

.overview-stat .stat-icon { font-size: 1.8em; }
.overview-stat .stat-number { font-size: 1.5em; font-weight: bold; }
.overview-stat .stat-label { font-size: 0.85em; opacity: 0.9; }

/* 等级图例 */
.bond-legend {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    padding: 12px 15px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 0.9em;
}

.legend-item { display: flex; align-items: center; gap: 6px; }

/* 等级徽章 */
.level-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: bold;
    color: white;
}
.level-badge.lv0 { background: #adb5bd; }
.level-badge.lv1 { background: #3498db; }
.level-badge.lv2 { background: #2ecc71; }
.level-badge.lv3 { background: linear-gradient(90deg, #f39c12, #e67e22); }

/* 羁绊对网格 */
.bond-pairs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 15px;
}

/* 羁绊卡片 */
.bond-card {
    background: #f8f9fa;
    border-radius: 10px;
    border: 2px solid #dee2e6;
    overflow: hidden;
    transition: all 0.3s;
}

.bond-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.bond-card[data-tier="1"] { background: #e8f4fd; border-color: #3498db; }
.bond-card[data-tier="2"] { background: #e8f8e8; border-color: #2ecc71; }
.bond-card[data-tier="3"] {
    background: linear-gradient(135deg, #fef9e7 0%, #fdebd0 100%);
    border-color: #f39c12;
}

.bond-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 15px;
    border-bottom: 1px solid rgba(0,0,0,0.06);
}

.bond-avatars {
    display: flex;
    align-items: center;
    gap: 8px;
}

.bond-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2em;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bond-link { font-size: 1.3em; }

.bond-body { padding: 15px; }

.bond-names {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 15px;
    font-size: 1.1em;
    font-weight: bold;
    color: #333;
}

.bond-vs { color: #999; font-size: 0.9em; }

.bond-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 15px;
}

.bond-stat {
    text-align: center;
    padding: 8px;
    background: white;
    border-radius: 6px;
}

.bond-stat-label {
    display: block;
    font-size: 0.75em;
    color: #666;
    margin-bottom: 4px;
}

.bond-stat-value {
    display: block;
    font-size: 1.1em;
    font-weight: bold;
    color: #333;
}

.bond-stat-value.positive { color: #2ecc71; }

/* 羁绊进度条 */
.bond-progress { margin-top: 10px; }

.bond-progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.8em;
    color: #666;
    margin-bottom: 6px;
}

.bond-next-level { color: #3498db; font-weight: bold; }

/* 空状态 */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #999;
}

.empty-icon { font-size: 4em; margin-bottom: 15px; opacity: 0.5; }
.empty-state p { margin-bottom: 8px; font-size: 1.1em; }
.empty-hint { font-size: 0.9em !important; color: #bbb !important; }

/* 羁绊升级动画 */
@keyframes bondLevelUp {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); box-shadow: 0 0 20px rgba(243, 156, 18, 0.5); }
    100% { transform: scale(1); }
}

.bond-card.level-up { animation: bondLevelUp 0.6s ease-out; }

/* 满级标记 */
.bond-card[data-tier="3"] .bond-next-level { color: #f39c12; }

/* 响应式 */
@media (max-width: 768px) {
    .bonds-overview { grid-template-columns: 1fr; }
    .bond-pairs-grid { grid-template-columns: 1fr; }
    .bond-stats { grid-template-columns: 1fr; }
}
```

---

## 4. JavaScript 逻辑

追加到 `frontend/js/app.js`：

```javascript
// ========== 羁绊系统 ==========

const BOND_TIERS = {
    0: { name: '陌生人', minDays: 0,   qualityBonus: 0,  salaryDiscount: 0  },
    1: { name: '同事',   minDays: 30,  qualityBonus: 3,  salaryDiscount: 0  },
    2: { name: '好友',   minDays: 60,  qualityBonus: 5,  salaryDiscount: 5  },
    3: { name: '知己',   minDays: 90,  qualityBonus: 8,  salaryDiscount: 10 },
};

function getBondTier(days) {
    if (days >= 90) return 3;
    if (days >= 60) return 2;
    if (days >= 30) return 1;
    return 0;
}

function getDaysToNextTier(days) {
    const tier = getBondTier(days);
    if (tier >= 3) return 0;
    return BOND_TIERS[tier + 1].minDays - days;
}

function getTierProgress(days) {
    const tier = getBondTier(days);
    if (tier >= 3) return 100;
    const currentMin = BOND_TIERS[tier].minDays;
    const nextMin = BOND_TIERS[tier + 1].minDays;
    return Math.min(100, ((days - currentMin) / (nextMin - currentMin)) * 100);
}

// 更新羁绊列表
async function updateBondList() {
    try {
        const agentsResult = await api.listAgents();
        const agents = agentsResult.agents || [];
        const container = document.getElementById('bond-pairs-list');
        const emptyState = document.getElementById('bond-empty');

        if (agents.length < 2) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        // 生成所有可能的员工对
        const pairs = [];
        for (let i = 0; i < agents.length; i++) {
            for (let j = i + 1; j < agents.length; j++) {
                const bondDays = Math.min(agents[i].bond_days, agents[j].bond_days);
                pairs.push({ emp1: agents[i], emp2: agents[j], bondDays });
            }
        }

        // 按羁绊天数排序
        pairs.sort((a, b) => b.bondDays - a.bondDays);

        // 检查是否全部为 Lv0
        if (pairs.every(p => p.bondDays === 0)) {
            container.innerHTML = '';
            emptyState.style.display = 'block';
            return;
        }

        emptyState.style.display = 'none';

        container.innerHTML = pairs.map(pair => {
            const tier = getBondTier(pair.bondDays);
            const daysToNext = getDaysToNextTier(pair.bondDays);
            const progress = getTierProgress(pair.bondDays);
            const t = BOND_TIERS[tier];
            const nextTier = tier < 3 ? tier + 1 : null;

            const progressText = tier >= 3 ? '已满级 ✨' : `距下一级还需 ${daysToNext} 天`;
            const nextLevelText = nextTier ? `→ Lv${nextTier} ${BOND_TIERS[nextTier].name}` : '';

            return `
                <div class="bond-card" data-tier="${tier}">
                    <div class="bond-header">
                        <div class="bond-avatars">
                            <div class="bond-avatar">👨‍💻</div>
                            <div class="bond-link">🤝</div>
                            <div class="bond-avatar">👩‍💻</div>
                        </div>
                        <span class="level-badge lv${tier}">Lv${tier} ${t.name}</span>
                    </div>
                    <div class="bond-body">
                        <div class="bond-names">
                            <span class="bond-name">${pair.emp1.name}</span>
                            <span class="bond-vs">×</span>
                            <span class="bond-name">${pair.emp2.name}</span>
                        </div>
                        <div class="bond-stats">
                            <div class="bond-stat">
                                <span class="bond-stat-label">协作天数</span>
                                <span class="bond-stat-value">${pair.bondDays} 天</span>
                            </div>
                            <div class="bond-stat">
                                <span class="bond-stat-label">质量加成</span>
                                <span class="bond-stat-value ${t.qualityBonus > 0 ? 'positive' : ''}">+${t.qualityBonus}%</span>
                            </div>
                            <div class="bond-stat">
                                <span class="bond-stat-label">薪资减免</span>
                                <span class="bond-stat-value ${t.salaryDiscount > 0 ? 'positive' : ''}">-${t.salaryDiscount}%</span>
                            </div>
                        </div>
                        <div class="bond-progress">
                            <div class="bond-progress-label">
                                <span>${progressText}</span>
                                <span class="bond-next-level">${nextLevelText}</span>
                            </div>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progress}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        // 更新概览
        const activePairs = pairs.filter(p => getBondTier(p.bondDays) > 0);
        document.getElementById('bond-pairs-count').textContent = activePairs.length;

        let maxQuality = 0, maxSalary = 0;
        activePairs.forEach(p => {
            const t = BOND_TIERS[getBondTier(p.bondDays)];
            if (t.qualityBonus > maxQuality) maxQuality = t.qualityBonus;
            if (t.salaryDiscount > maxSalary) maxSalary = t.salaryDiscount;
        });
        document.getElementById('bond-max-quality').textContent = `+${maxQuality}%`;
        document.getElementById('bond-max-salary').textContent = `${maxSalary}%`;

    } catch (e) {
        console.error('更新羁绊列表失败:', e);
    }
}

// 羁绊升级通知
function showBondLevelUp(emp1Name, emp2Name, newTier) {
    const t = BOND_TIERS[newTier];
    const messages = {
        1: `🤝 ${emp1Name} 和 ${emp2Name} 成为了同事！项目质量 +3%`,
        2: `🎉 ${emp1Name} 和 ${emp2Name} 成为了好友！项目质量 +5%，薪资 -5%`,
        3: `💖 ${emp1Name} 和 ${emp2Name} 成为了知己！项目质量 +8%，薪资 -10%`,
    };
    showNotification(messages[newTier] || '羁绊升级！', 'positive');
}

// 扩展 showTab 以支持羁绊标签
const _originalShowTab = window.showTab;
window.showTab = function(tabName) {
    _originalShowTab(tabName);
    if (tabName === 'bonds') updateBondList();
};

window.updateBondList = updateBondList;
window.showBondLevelUp = showBondLevelUp;
```

---

## 5. 羁绊事件文案

### 羁绊升级通知

| 场景 | 通知文案 | 类型 |
|------|---------|------|
| Lv0 → Lv1 | `"🤝 {A} 和 {B} 从陌生人变成了同事！项目质量 +3%"` | positive |
| Lv1 → Lv2 | `"🎉 {A} 和 {B} 成为了好朋友！项目质量 +5%，薪资减免 -5%"` | positive |
| Lv2 → Lv3 | `"💖 {A} 和 {B} 成为了知己！项目质量 +8%，薪资减免 -10%"` | positive |

### 羁绊加成提示

| 场景 | 提示文案 |
|------|---------|
| 项目完成（有羁绊加成） | `"🤝 羁绊加成：{A} × {B} 贡献 +{bonus}% 质量"` |
| 薪资结算（有羁绊减免） | `"💰 羁绊减免：今日薪资节省 $${amount}"` |

### 随机事件扩展（新增事件，后续加入 events.json）

| 事件 | 类型 | 文案 | 效果 |
|------|------|------|------|
| 深夜加班 | 正面 | `"🌙 {A} 和 {B} 一起加班到深夜，默契大增！羁绊 +5 天"` | 指定 pair bond_days +5 |
| 团建活动 | 正面 | `"🎪 团建活动让团队更紧密了！所有羁绊 +3 天"` | 所有 pair bond_days +3 |
| 意见不合 | 负面 | `"😤 {A} 和 {B} 在项目方案上起了争执..."` | 指定 pair bond_days -2（最低 0） |
| 默契配合 | 正面 | `"✨ {A} 和 {B} 配合默契，项目质量临时 +5%！"` | 当前项目质量 +5%（临时） |

---

## 6. 文件修改清单

| 文件 | 操作 | 行数估计 | 内容 |
|------|------|---------|------|
| `frontend/index.html` | 修改 | +2 行 | 新增"团队羁绊"按钮 + `tab-bonds` 标签页 |
| `frontend/css/style.css` | 追加 | ~130 行 | 羁绊面板完整 CSS |
| `frontend/js/app.js` | 追加 | ~100 行 | 羁绊等级计算 + 列表渲染 + 升级通知 |
| `backend/routes/company_routes.py` | 已有 | — | `GET /api/company/bond/<emp1>/<emp2>` 已存在 |
| `backend/models/company.py` | 已有 | — | `PAIR_BOND_TIERS` + `bond_pairs` + 计算函数已存在 |

---

_羁绊 UI 面板设计完毕，后端 API 已就位，全栈开发可以直接落前端。_
