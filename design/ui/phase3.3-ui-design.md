# Phase 3.3 UI 设计稿

**版本**: v1.0  
**日期**: 2026-04-23  
**创意总监**: 创意总监

---

## 1. 总体布局

在现有 `index.html` 的 tabs 区域新增 3 个 tab-content：

```
现有结构:
├── tab-agents (员工管理)
├── tab-projects (项目管理)
├── tab-equipment (设备中心) ← 新增
├── tab-brand (品牌管理)     ← 新增
└── tab-funding (融资中心)   ← 新增
```

主操作面板新增 3 个按钮：

```
现有: [📅 下一天] [👥 雇佣员工] [📋 查看项目] [🏢 升级办公室]
新增: [🔧 设备中心] [🏷️ 品牌管理] [💹 融资中心]
```

---

## 2. 设备中心 (tab-equipment)

```html
<div id="tab-equipment" class="tab-content">
    <h2>🔧 设备中心</h2>
    <p class="tab-desc">购买设备提升公司效率。设备一次性购买，永久生效。</p>
    <div class="current-bonus">
        当前设备总加成: <span id="equipment-total-bonus">0%</span>
        （上限 150%）
    </div>
    <div id="equipment-list" class="cards-grid">
        <!-- 动态渲染 -->
    </div>
</div>
```

### 设备卡片样式

```
┌────────────────────────────────────────┐
│ 🔧 高速网络                            │
│ ─────────────────────────────────────  │
│ 价格:    $10,000                       │
│ 效果:    项目进度 +5%                  │
│ 解锁:    无限制                        │
│                                        │
│ [🛒 立即购买]  ← 未购买时              │
│ [✅ 已购买]    ← 已购买时（灰色禁用）  │
└────────────────────────────────────────┘
```

卡片颜色：未购买 = 白底蓝边，已购买 = 浅绿底绿边

---

## 3. 品牌管理 (tab-brand)

```html
<div id="tab-brand" class="tab-content">
    <h2>🏷️ 品牌管理</h2>
    
    <!-- 品牌状态卡片 -->
    <div class="brand-status-card">
        <div class="brand-level-display">
            <span class="brand-icon" id="brand-icon">🌑</span>
            <div>
                <div class="brand-level-text">
                    Lv<span id="brand-level">0</span> - 
                    <span id="brand-name">无名小卒</span>
                </div>
                <div class="brand-desc" id="brand-desc">还没人知道你们的存在...</div>
            </div>
        </div>
        <div class="brand-stats">
            <div class="brand-stat">
                <span class="stat-label">报酬倍率</span>
                <span class="stat-value" id="brand-multiplier">1.0x</span>
            </div>
            <div class="brand-stat">
                <span class="stat-label">好项目加成</span>
                <span class="stat-value" id="brand-bonus">+0%</span>
            </div>
            <div class="brand-stat">
                <span class="stat-label">日维护费</span>
                <span class="stat-value" id="brand-daily-cost">$0/天</span>
            </div>
            <div class="brand-stat">
                <span class="stat-label">下次维护</span>
                <span class="stat-value" id="brand-next-check">--</span>
            </div>
        </div>
    </div>
    
    <!-- 品牌进度条 -->
    <div class="brand-progress">
        <div class="progress-label">品牌等级进度</div>
        <div class="progress-bar">
            <div class="progress-fill" id="brand-progress-fill" style="width: 0%"></div>
        </div>
        <div class="progress-text">
            <span id="brand-progress-current">0</span> / 5
        </div>
    </div>
    
    <!-- 营销活动 -->
    <h3>📢 营销活动</h3>
    <div id="marketing-list" class="cards-grid">
        <!-- 动态渲染 -->
    </div>
    
    <!-- 续费 -->
    <div class="brand-maintenance">
        <h3>💳 品牌维护</h3>
        <div class="maintenance-row">
            <span>续费天数:</span>
            <input type="number" id="maintenance-days" value="30" min="7" max="365" step="7">
            <span>费用: $<span id="maintenance-cost">0</span></span>
            <button class="btn btn-primary" onclick="maintainBrand()">续费</button>
        </div>
    </div>
</div>
```

### 品牌状态卡片样式

```
┌────────────────────────────────────────────┐
│ 🌔 Lv3 - 知名公司                          │
│ 行业大会上有人主动来交换名片               │
│                                            │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐      │
│ │报酬  │ │好项目│ │维护费│ │下次  │      │
│ │1.3x  │ │+30%  │ │$2k/天│ │23天后│      │
│ └──────┘ └──────┘ └──────┘ └──────┘      │
│                                            │
│ ████████████████░░░░░░░░░░░░░░  3.0 / 5   │
└────────────────────────────────────────────┘
```

### 营销活动卡片

```
┌────────────────────────────────┐
│ 📢 社交媒体推广               │
│ 成本: $15,000                  │
│ 效果: 品牌等级 +0.5            │
│ [执行活动]                     │
└────────────────────────────────┘
```

---

## 4. 融资中心 (tab-funding)

```html
<div id="tab-funding" class="tab-content">
    <h2>💹 融资中心</h2>
    
    <!-- 股权概览 -->
    <div class="equity-overview">
        <div class="equity-chart">
            <div class="equity-remaining">
                <span class="equity-percent" id="equity-remaining-pct">100%</span>
                <span class="equity-label">你的股权</span>
            </div>
            <div class="equity-sold">
                <span class="equity-percent" id="equity-sold-pct">0%</span>
                <span class="equity-label">已出让</span>
            </div>
        </div>
        <div class="equity-stats">
            <div class="equity-stat">
                <span class="stat-label">季度分红</span>
                <span class="stat-value" id="dividend-quarterly">$0</span>
            </div>
            <div class="equity-stat">
                <span class="stat-label">累计欠款</span>
                <span class="stat-value warning" id="dividend-arrears">$0</span>
            </div>
            <div class="equity-stat">
                <span class="stat-label">公司估值</span>
                <span class="stat-value" id="company-valuation">$0</span>
            </div>
        </div>
    </div>
    
    <!-- 股权进度条 -->
    <div class="equity-progress">
        <div class="progress-label">股权稀释进度</div>
        <div class="progress-bar danger-zone">
            <div class="progress-fill" id="equity-progress-fill" style="width: 0%"></div>
            <div class="danger-marker" style="left: 50%">50%</div>
        </div>
        <div class="progress-text">超过 50% 将触发"创始人出局"结局</div>
    </div>
    
    <!-- 融资轮次 -->
    <h3>🚀 融资轮次</h3>
    <div id="funding-rounds" class="cards-grid">
        <!-- 动态渲染 -->
    </div>
    
    <!-- 回购 -->
    <div class="buyback-section">
        <h3>🔄 股权回购</h3>
        <div class="buyback-row">
            <span>回购金额: $</span>
            <input type="number" id="buyback-amount" value="100000" min="10000" step="10000">
            <span>可回购: <span id="buyback-equity">0%</span> 股权</span>
            <button class="btn btn-warning" onclick="buybackEquity()">确认回购</button>
        </div>
    </div>
    
    <!-- 投资者列表 -->
    <h3>👥 投资者</h3>
    <div id="investors-list" class="cards-grid">
        <!-- 动态渲染 -->
    </div>
</div>
```

### 融资轮次卡片

```
┌────────────────────────────────────────┐
│ 🌱 种子轮                              │
│ ─────────────────────────────────────  │
│ 融资金额: $100,000                     │
│ 出让股权: 10%                          │
│ 季度分红: 净利润的 5%                  │
│ 解锁条件: 第 10 天                     │
│                                        │
│ [🤝 申请融资]  ← 已解锁时              │
│ [🔒 未解锁]    ← 未解锁时（灰色禁用）  │
└────────────────────────────────────────┘
```

### 股权概览样式

```
┌──────────────────────────────────────────┐
│  ┌──────────────┐    ┌──────────────┐   │
│  │   90%        │    │   10%        │   │
│  │  你的股权     │    │  已出让       │   │
│  └──────────────┘    └──────────────┘   │
│                                          │
│  季度分红: $5,000  │ 欠款: $0 │ 估值: $500k │
│                                          │
│  ████████████████████░░░░░░░░░░░░░░░░░░  │
│  股权稀释进度          ↑ 50% 危险线      │
└──────────────────────────────────────────┘
```

---

## 5. 状态面板扩展

在现有 4 个 status-card 之后新增 2 个：

```html
<div class="status-card">
    <div class="status-icon">🏷️</div>
    <div class="status-info">
        <div class="status-label">品牌</div>
        <div class="status-value" id="brand-status">Lv0 无名小卒</div>
    </div>
</div>

<div class="status-card">
    <div class="status-icon">💹</div>
    <div class="status-info">
        <div class="status-label">股权</div>
        <div class="status-value" id="equity-status">100% 控股</div>
    </div>
</div>
```

---

## 6. CSS 新增样式要点

```css
/* 品牌状态卡片 */
.brand-status-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 16px;
}

/* 股权危险区标记 */
.danger-zone .danger-marker {
    position: absolute;
    top: -18px;
    color: #ff4757;
    font-size: 11px;
    font-weight: bold;
}

.danger-zone .progress-fill {
    background: linear-gradient(90deg, #2ed573 0%, #ffa502 50%, #ff4757 100%);
}

/* 设备已购买状态 */
.equipment-card.purchased {
    background: #f0fff4;
    border-color: #38a169;
}

.equipment-card.purchased .buy-btn {
    background: #cbd5e0;
    color: #718096;
    cursor: not-allowed;
}

/* 融资未解锁 */
.funding-card.locked {
    opacity: 0.5;
    pointer-events: none;
}
```

---

_设计稿完毕，全栈开发可以直接按此实现前端。_
