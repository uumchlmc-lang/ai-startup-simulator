# 难度选择 UI 面板设计

**版本**: v1.0  
**日期**: 2026-04-25  
**创意总监**: 创意总监  
**用途**: 全栈开发直接落前端的完整设计稿

---

## 1. 后端 API 现状（已实现，commit 7cbf54e）

### API 路由（`backend/routes/difficulty_routes.py`）

| API | 方法 | 路径 | 返回 |
|-----|------|------|------|
| 当前难度 | GET | `/api/difficulty` | `{difficulty: "normal", config: {...}}` |
| 设置难度 | POST | `/api/difficulty/<mode>` | `{success: true, difficulty, cash}` |
| 全部配置 | GET | `/api/difficulty/config` | `{difficulties: {easy, normal, hard}}` |

**mode 参数**: `easy` / `normal` / `hard` / `custom`

**自定义模式请求体**:
```json
{
    "initial_cash": 75000,
    "reward_multiplier": 1.0,
    "salary_multiplier": 1.0,
    "equipment_price_multiplier": 1.0,
    "brand_maintenance_multiplier": 1.0
}
```

### DIFFICULTY_CONFIG（`backend/models/company.py` 第 29-49 行）

| 参数 | 简单 (easy) | 普通 (normal) | 困难 (hard) |
|------|------------|--------------|------------|
| 初始资金 | $100,000 | $75,000 | $35,000 |
| 报酬倍率 | ×1.3 | ×1.0 | ×0.7 |
| 薪资倍率 | ×0.8 | ×1.0 | ×1.3 |
| 设备价格倍率 | ×0.8 | ×1.0 | ×1.3 |
| 品牌维护费倍率 | ×0.7 | ×1.0 | ×1.3 |

### Company 数据模型（`backend/models/company.py` 第 25-26 行）

```python
difficulty: str = "normal"  # easy/normal/hard/custom
difficulty_settings: Dict[str, float] = field(default_factory=dict)  # 自定义参数
```

---

## 2. 整体设计思路

难度选择页面是**新游戏开始时的第一步**，应该：
- 在 `index.html` 中以**模态弹窗**形式展示（游戏启动时自动弹出）
- 3 种预设难度用**卡片**直观对比
- 自定义难度用**滑块**精细调节
- 选择后调用 `POST /api/difficulty/<mode>` 确认

---

## 3. index.html 修改

### 3.1 新增难度选择弹窗

在游戏结束弹窗 (`#game-over`) 之后添加：

```html
<!-- 难度选择弹窗 -->
<div id="difficulty-select" class="modal" style="display:none;">
    <div class="modal-content difficulty-modal">
        <h2>🎮 选择难度</h2>
        <p class="modal-subtitle">难度影响初始资金、报酬、薪资等参数。选择后不可更改。</p>

        <!-- 预设难度卡片 -->
        <div class="difficulty-cards">
            <!-- 简单 -->
            <div class="difficulty-card easy" onclick="selectDifficulty('easy', this)">
                <div class="difficulty-icon">😊</div>
                <div class="difficulty-name">简单</div>
                <div class="difficulty-tag">轻松创业</div>
                <div class="difficulty-desc">适合新手玩家，更多容错空间</div>
                <div class="difficulty-params">
                    <div class="param-row positive">💰 初始资金 $100,000</div>
                    <div class="param-row positive">📈 报酬 ×1.3</div>
                    <div class="param-row positive">💵 薪资 ×0.8</div>
                    <div class="param-row positive">🔧 设备价格 ×0.8</div>
                    <div class="param-row positive">🏷️ 维护费 ×0.7</div>
                </div>
            </div>

            <!-- 普通 -->
            <div class="difficulty-card normal selected" onclick="selectDifficulty('normal', this)">
                <div class="difficulty-icon">🎯</div>
                <div class="difficulty-name">普通</div>
                <div class="difficulty-tag recommended">推荐</div>
                <div class="difficulty-desc">标准创业体验，平衡挑战与乐趣</div>
                <div class="difficulty-params">
                    <div class="param-row">💰 初始资金 $75,000</div>
                    <div class="param-row">📈 报酬 ×1.0</div>
                    <div class="param-row">💵 薪资 ×1.0</div>
                    <div class="param-row">🔧 设备价格 ×1.0</div>
                    <div class="param-row">🏷️ 维护费 ×1.0</div>
                </div>
            </div>

            <!-- 困难 -->
            <div class="difficulty-card hard" onclick="selectDifficulty('hard', this)">
                <div class="difficulty-icon">🔥</div>
                <div class="difficulty-name">困难</div>
                <div class="difficulty-tag">硬核挑战</div>
                <div class="difficulty-desc">适合老手，步步惊心</div>
                <div class="difficulty-params">
                    <div class="param-row negative">💰 初始资金 $35,000</div>
                    <div class="param-row negative">📈 报酬 ×0.7</div>
                    <div class="param-row negative">💵 薪资 ×1.3</div>
                    <div class="param-row negative">🔧 设备价格 ×1.3</div>
                    <div class="param-row negative">🏷️ 维护费 ×1.3</div>
                </div>
            </div>
        </div>

        <!-- 自定义难度切换 -->
        <div class="custom-toggle">
            <button class="btn btn-outline" id="custom-toggle-btn" onclick="toggleCustomDifficulty()">
                ⚙️ 自定义难度
            </button>
        </div>

        <!-- 自定义难度面板 -->
        <div id="custom-difficulty-panel" class="custom-panel" style="display:none;">
            <h3>⚙️ 自定义参数</h3>
            <p class="custom-hint">拖动滑块调整参数，实时预览效果</p>

            <div class="custom-sliders">
                <!-- 初始资金 -->
                <div class="slider-group">
                    <div class="slider-header">
                        <label>💰 初始资金</label>
                        <span class="slider-value" id="cash-value">$75,000</span>
                    </div>
                    <input type="range" id="custom-cash" min="10000" max="200000" step="5000" value="75000"
                           oninput="updateCustomDifficulty()">
                    <div class="slider-range">
                        <span>$10k</span>
                        <span>$200k</span>
                    </div>
                </div>

                <!-- 报酬倍率 -->
                <div class="slider-group">
                    <div class="slider-header">
                        <label>📈 报酬倍率</label>
                        <span class="slider-value" id="reward-value">×1.0</span>
                    </div>
                    <input type="range" id="custom-reward" min="0.5" max="2.0" step="0.1" value="1.0"
                           oninput="updateCustomDifficulty()">
                    <div class="slider-range">
                        <span>×0.5</span>
                        <span>×2.0</span>
                    </div>
                </div>

                <!-- 薪资倍率 -->
                <div class="slider-group">
                    <div class="slider-header">
                        <label>💵 薪资倍率</label>
                        <span class="slider-value" id="salary-value">×1.0</span>
                    </div>
                    <input type="range" id="custom-salary" min="0.5" max="2.0" step="0.1" value="1.0"
                           oninput="updateCustomDifficulty()">
                    <div class="slider-range">
                        <span>×0.5</span>
                        <span>×2.0</span>
                    </div>
                </div>

                <!-- 设备价格倍率 -->
                <div class="slider-group">
                    <div class="slider-header">
                        <label>🔧 设备价格倍率</label>
                        <span class="slider-value" id="equipment-value">×1.0</span>
                    </div>
                    <input type="range" id="custom-equipment" min="0.5" max="2.0" step="0.1" value="1.0"
                           oninput="updateCustomDifficulty()">
                    <div class="slider-range">
                        <span>×0.5</span>
                        <span>×2.0</span>
                    </div>
                </div>

                <!-- 品牌维护费倍率 -->
                <div class="slider-group">
                    <div class="slider-header">
                        <label>🏷️ 品牌维护费倍率</label>
                        <span class="slider-value" id="brand-value">×1.0</span>
                    </div>
                    <input type="range" id="custom-brand" min="0.5" max="2.0" step="0.1" value="1.0"
                           oninput="updateCustomDifficulty()">
                    <div class="slider-range">
                        <span>×0.5</span>
                        <span>×2.0</span>
                    </div>
                </div>
            </div>

            <!-- 自定义难度预览 -->
            <div class="custom-preview">
                <h4>📊 参数对比（vs 普通难度）</h4>
                <div class="preview-grid" id="custom-preview-grid">
                    <!-- 动态渲染 -->
                </div>
            </div>
        </div>

        <!-- 确认按钮 -->
        <div class="difficulty-actions">
            <button class="btn btn-primary btn-lg" id="confirm-difficulty-btn" onclick="confirmDifficulty()">
                🚀 开始创业
            </button>
        </div>
    </div>
</div>
```

---

## 4. CSS 新增样式

追加到 `frontend/css/style.css`：

```css
/* ========== 难度选择弹窗 ========== */

.difficulty-modal {
    max-width: 900px;
    max-height: 90vh;
    overflow-y: auto;
    padding: 30px;
}

.modal-subtitle {
    color: #666;
    font-size: 0.95em;
    margin-bottom: 25px;
}

/* 难度卡片 */
.difficulty-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}

.difficulty-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    border: 3px solid #dee2e6;
    cursor: pointer;
    transition: all 0.3s;
    text-align: center;
    position: relative;
}

.difficulty-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.difficulty-card.selected {
    border-color: #667eea;
    background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 100%);
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
}

/* 简单难度 */
.difficulty-card.easy.selected {
    border-color: #2ecc71;
    background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
    box-shadow: 0 4px 16px rgba(46, 204, 113, 0.2);
}

/* 困难难度 */
.difficulty-card.hard.selected {
    border-color: #e74c3c;
    background: linear-gradient(135deg, #fff5f5 0%, #ffffff 100%);
    box-shadow: 0 4px 16px rgba(231, 76, 60, 0.2);
}

.difficulty-icon {
    font-size: 3em;
    margin-bottom: 10px;
}

.difficulty-name {
    font-size: 1.4em;
    font-weight: bold;
    color: #333;
    margin-bottom: 5px;
}

.difficulty-tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 12px;
    font-size: 0.8em;
    background: #e8f4fd;
    color: #3498db;
    margin-bottom: 10px;
}

.difficulty-tag.recommended {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
}

.difficulty-desc {
    font-size: 0.85em;
    color: #666;
    margin-bottom: 15px;
}

.difficulty-params {
    text-align: left;
}

.param-row {
    padding: 5px 0;
    font-size: 0.9em;
    color: #666;
    border-bottom: 1px solid #f0f0f0;
}

.param-row:last-child {
    border-bottom: none;
}

.param-row.positive {
    color: #2ecc71;
    font-weight: bold;
}

.param-row.negative {
    color: #e74c3c;
    font-weight: bold;
}

/* 自定义难度切换 */
.custom-toggle {
    text-align: center;
    margin-bottom: 20px;
}

.btn-outline {
    background: transparent;
    border: 2px solid #667eea;
    color: #667eea;
    padding: 10px 24px;
    border-radius: 8px;
    font-size: 1em;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-outline:hover {
    background: #667eea;
    color: white;
}

.btn-outline.active {
    background: #667eea;
    color: white;
}

/* 自定义难度面板 */
.custom-panel {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    border: 2px dashed #667eea;
}

.custom-panel h3 {
    margin-bottom: 5px;
    color: #333;
}

.custom-hint {
    color: #999;
    font-size: 0.85em;
    margin-bottom: 20px;
}

/* 滑块组 */
.slider-group {
    margin-bottom: 20px;
}

.slider-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.slider-header label {
    font-weight: bold;
    color: #333;
}

.slider-value {
    font-weight: bold;
    color: #667eea;
    font-size: 1.1em;
    min-width: 60px;
    text-align: right;
}

.slider-group input[type="range"] {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: #e0e0e0;
    outline: none;
    -webkit-appearance: none;
}

.slider-group input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #667eea;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.slider-group input[type="range"]::-moz-range-thumb {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #667eea;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.slider-range {
    display: flex;
    justify-content: space-between;
    font-size: 0.75em;
    color: #999;
    margin-top: 4px;
}

/* 自定义预览 */
.custom-preview {
    background: white;
    border-radius: 8px;
    padding: 15px;
    margin-top: 20px;
}

.custom-preview h4 {
    margin-bottom: 12px;
    color: #333;
    font-size: 0.95em;
}

.preview-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
}

.preview-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: #f8f9fa;
    border-radius: 6px;
    font-size: 0.9em;
}

.preview-label {
    color: #666;
}

.preview-value {
    font-weight: bold;
}

.preview-value.better {
    color: #2ecc71;
}

.preview-value.worse {
    color: #e74c3c;
}

.preview-value.same {
    color: #999;
}

/* 确认按钮 */
.difficulty-actions {
    text-align: center;
    padding-top: 10px;
}

.btn-lg {
    padding: 14px 40px;
    font-size: 1.15em;
}

/* 响应式 */
@media (max-width: 768px) {
    .difficulty-cards {
        grid-template-columns: 1fr;
    }
    
    .preview-grid {
        grid-template-columns: 1fr;
    }
    
    .difficulty-modal {
        padding: 20px;
    }
}
```

---

## 5. JavaScript 逻辑

追加到 `frontend/js/app.js`：

```javascript
// ========== 难度选择系统 ==========

let selectedDifficulty = 'normal';
let isCustomMode = false;

// 显示难度选择弹窗（游戏启动时调用）
function showDifficultySelect() {
    document.getElementById('difficulty-select').style.display = 'flex';
}

// 选择预设难度
function selectDifficulty(mode, card) {
    isCustomMode = false;
    selectedDifficulty = mode;
    
    // 更新选中状态
    document.querySelectorAll('.difficulty-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    
    // 隐藏自定义面板
    document.getElementById('custom-difficulty-panel').style.display = 'none';
    document.getElementById('custom-toggle-btn').classList.remove('active');
}

// 切换自定义难度
function toggleCustomDifficulty() {
    const panel = document.getElementById('custom-difficulty-panel');
    const btn = document.getElementById('custom-toggle-btn');
    
    if (panel.style.display === 'none') {
        panel.style.display = 'block';
        btn.classList.add('active');
        btn.textContent = '⚙️ 收起自定义';
        isCustomMode = true;
        selectedDifficulty = 'custom';
        
        // 取消预设卡片的选中
        document.querySelectorAll('.difficulty-card').forEach(c => c.classList.remove('selected'));
        
        updateCustomDifficulty();
    } else {
        panel.style.display = 'none';
        btn.classList.remove('active');
        btn.textContent = '⚙️ 自定义难度';
        isCustomMode = false;
        selectedDifficulty = 'normal';
        
        // 恢复普通难度选中
        document.querySelector('.difficulty-card.normal').classList.add('selected');
    }
}

// 更新自定义难度预览
function updateCustomDifficulty() {
    const cash = parseInt(document.getElementById('custom-cash').value);
    const reward = parseFloat(document.getElementById('custom-reward').value);
    const salary = parseFloat(document.getElementById('custom-salary').value);
    const equipment = parseFloat(document.getElementById('custom-equipment').value);
    const brand = parseFloat(document.getElementById('custom-brand').value);
    
    // 更新显示值
    document.getElementById('cash-value').textContent = '$' + cash.toLocaleString();
    document.getElementById('reward-value').textContent = '×' + reward.toFixed(1);
    document.getElementById('salary-value').textContent = '×' + salary.toFixed(1);
    document.getElementById('equipment-value').textContent = '×' + equipment.toFixed(1);
    document.getElementById('brand-value').textContent = '×' + brand.toFixed(1);
    
    // 更新预览对比
    const normalCash = 75000;
    const grid = document.getElementById('custom-preview-grid');
    
    const items = [
        { label: '💰 初始资金', value: '$' + cash.toLocaleString(), normal: normalCash, current: cash, isMultiplier: false },
        { label: '📈 报酬', value: '×' + reward.toFixed(1), normal: 1.0, current: reward, isMultiplier: true },
        { label: '💵 薪资', value: '×' + salary.toFixed(1), normal: 1.0, current: salary, isMultiplier: true },
        { label: '🔧 设备价格', value: '×' + equipment.toFixed(1), normal: 1.0, current: equipment, isMultiplier: true },
        { label: '🏷️ 维护费', value: '×' + brand.toFixed(1), normal: 1.0, current: brand, isMultiplier: true },
    ];
    
    grid.innerHTML = items.map(item => {
        let cls = 'same';
        if (item.isMultiplier) {
            // 对玩家有利的（报酬高、薪资低、设备便宜、维护费低）标绿
            if (item.label.includes('报酬') && item.current > item.normal) cls = 'better';
            else if (item.label.includes('报酬')) cls = 'worse';
            else if ((item.label.includes('薪资') || item.label.includes('设备') || item.label.includes('维护')) && item.current < item.normal) cls = 'better';
            else if (item.label.includes('薪资') || item.label.includes('设备') || item.label.includes('维护')) cls = 'worse';
        } else {
            cls = item.current > item.normal ? 'better' : (item.current < item.normal ? 'worse' : 'same');
        }
        
        return `<div class="preview-item">
            <span class="preview-label">${item.label}</span>
            <span class="preview-value ${cls}">${item.value}</span>
        </div>`;
    }).join('');
}

// 确认难度并开始游戏
async function confirmDifficulty() {
    const btn = document.getElementById('confirm-difficulty-btn');
    btn.disabled = true;
    btn.textContent = '🚀 启动中...';
    
    try {
        let mode = selectedDifficulty;
        let body = {};
        
        if (mode === 'custom') {
            body = {
                initial_cash: parseInt(document.getElementById('custom-cash').value),
                reward_multiplier: parseFloat(document.getElementById('custom-reward').value),
                salary_multiplier: parseFloat(document.getElementById('custom-salary').value),
                equipment_price_multiplier: parseFloat(document.getElementById('custom-equipment').value),
                brand_maintenance_multiplier: parseFloat(document.getElementById('custom-brand').value),
            };
        }
        
        const response = await fetch(`/api/difficulty/${mode}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 关闭弹窗
            document.getElementById('difficulty-select').style.display = 'none';
            
            // 开始新游戏
            const gameResult = await api.newGame();
            if (gameResult.success) {
                updateUI(gameResult.company);
                showNotification(`🎮 难度: ${getDifficultyName(mode)} | 初始资金: $${result.cash.toLocaleString()}`, 'success');
            }
        } else {
            showNotification(`❌ ${result.error}`, 'error');
            btn.disabled = false;
            btn.textContent = '🚀 开始创业';
        }
    } catch (e) {
        showNotification(`❌ 错误: ${e.message}`, 'error');
        btn.disabled = false;
        btn.textContent = '🚀 开始创业';
    }
}

// 获取难度名称
function getDifficultyName(mode) {
    const names = { easy: '简单', normal: '普通', hard: '困难', custom: '自定义' };
    return names[mode] || mode;
}

// 导出
window.showDifficultySelect = showDifficultySelect;
window.selectDifficulty = selectDifficulty;
window.toggleCustomDifficulty = toggleCustomDifficulty;
window.updateCustomDifficulty = updateCustomDifficulty;
window.confirmDifficulty = confirmDifficulty;
```

---

## 6. 启动流程修改

在 `app.js` 的 `DOMContentLoaded` 中，替换现有的 `startNewGame()` 直接调用逻辑：

```javascript
// 初始化
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🎮 AI 创业模拟器启动...');
    
    // 尝试加载游戏
    const loaded = await api.loadGame();
    if (loaded && loaded.success) {
        console.log('✅ 游戏已加载');
        updateUI(loaded.company);
        setTimeout(() => {
            updateAgentsList();
            updateProjectsList();
        }, 500);
    } else {
        // 无存档 → 显示难度选择
        showDifficultySelect();
    }
    
    showNotification('🎮 欢迎来到 AI 创业模拟器！', 'info');
});
```

---

## 7. 文件修改清单

| 文件 | 操作 | 行数估计 | 内容 |
|------|------|---------|------|
| `frontend/index.html` | 修改 | +120 行 | 新增难度选择弹窗（3 卡片 + 自定义面板 + 滑块） |
| `frontend/css/style.css` | 追加 | ~200 行 | 难度选择完整 CSS（含滑块样式、卡片动画、预览网格） |
| `frontend/js/app.js` | 修改+追加 | ~120 行 | 难度选择逻辑 + 启动流程修改 |
| `backend/routes/difficulty_routes.py` | 已有 | — | 3 个 API 端点已存在 |
| `backend/models/company.py` | 已有 | — | `DIFFICULTY_CONFIG` + `difficulty` + `difficulty_settings` 已存在 |

---

_难度选择 UI 面板设计完毕，后端 API 已就位（commit 7cbf54e），全栈开发可以直接落前端。_
