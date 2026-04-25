# Phase 3.5 难度选择系统 — 技术设计文档

**版本**: v1.0  
**日期**: 2026-04-25  
**产品经理**: 产品经理  
**状态**: 待开发

---

## 1. 范围

Phase 3.5 实现 4 种难度模式：

| 模式 | 说明 | 优先级 |
|------|------|--------|
| 简单模式 | 新手友好，初始资金充足，项目报酬高 | P0 |
| 普通模式 | 默认难度，平衡体验 | P0 |
| 困难模式 | 挑战模式，初始资金紧张，项目报酬低 | P0 |
| 自定义模式 | 玩家自由调整各项参数 | P1 |

**已有基础**：当前游戏无难度系统，所有游戏使用固定参数（初始 $75k，倍率 1.0x）。

---

## 2. 数据模型

```python
# Company dataclass 新增
difficulty: str = "normal"  # 难度模式: easy/normal/hard/custom
difficulty_settings: Dict[str, float] = field(default_factory=dict)  # 自定义难度参数
```

**难度配置**：
```python
DIFFICULTY_CONFIG = {
    "easy": {
        "initial_cash": 100000,
        "project_reward_mult": 1.3,
        "salary_mult": 0.8,
        "equipment_price_mult": 0.8,
        "brand_maintenance_mult": 0.7,
        "quality_requirement": 0.8,  # 宽松：质量要求降低 20%
        "event_frequency": 0.7,  # 低频率
        "project_difficulty_mult": 0.8,  # 项目难度降低
    },
    "normal": {
        "initial_cash": 75000,
        "project_reward_mult": 1.0,
        "salary_mult": 1.0,
        "equipment_price_mult": 1.0,
        "brand_maintenance_mult": 1.0,
        "quality_requirement": 1.0,
        "event_frequency": 1.0,
        "project_difficulty_mult": 1.0,
    },
    "hard": {
        "initial_cash": 25000,
        "project_reward_mult": 0.7,
        "salary_mult": 1.3,
        "equipment_price_mult": 1.3,
        "brand_maintenance_mult": 1.5,
        "quality_requirement": 1.2,  # 严格：质量要求提高 20%
        "event_frequency": 1.5,  # 高频率
        "project_difficulty_mult": 1.3,  # 项目难度提高
    },
    "custom": {
        "initial_cash": 75000,  # 默认值，玩家可调整
        "project_reward_mult": 1.0,
        "salary_mult": 1.0,
        "equipment_price_mult": 1.0,
        "brand_maintenance_mult": 1.0,
        "quality_requirement": 1.0,
        "event_frequency": 1.0,
        "project_difficulty_mult": 1.0,
    },
}
```

---

## 3. 难度参数详解

| 参数 | 简单 | 普通 | 困难 | 说明 |
|------|------|------|------|------|
| 初始资金 | $100,000 | $75,000 | $25,000 | 游戏开始时的现金 |
| 项目报酬倍率 | 1.3x | 1.0x | 0.7x | 项目完成时的报酬乘数 |
| 员工薪资倍率 | 0.8x | 1.0x | 1.3x | 员工每日薪资乘数 |
| 设备价格倍率 | 0.8x | 1.0x | 1.3x | 设备购买价格乘数 |
| 品牌维护费倍率 | 0.7x | 1.0x | 1.5x | 品牌日维护费乘数 |
| 质量要求 | 宽松 (0.8) | 正常 (1.0) | 严格 (1.2) | 项目质量计算乘数 |
| 事件频率 | 低 (0.7) | 正常 (1.0) | 高 (1.5) | 随机事件触发概率乘数 |
| 项目难度 | 简单 (0.8) | 正常 (1.0) | 困难 (1.3) | 项目难度对进度的惩罚乘数 |

---

## 4. 难度应用位置

### 4.1 新游戏创建

```python
def new_game(self, company_name: str = "AI 创业公司", difficulty: str = "normal") -> Company:
    """开始新游戏（支持难度选择）"""
    self.company = Company(name=company_name, difficulty=difficulty)
    
    # 应用难度配置
    config = DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])
    self.company.cash = config["initial_cash"]
    
    # ... 其余逻辑不变 ...
```

### 4.2 项目报酬计算

```python
def complete_project(self, project_id: str) -> float:
    """完成项目，返回实际报酬"""
    # ... 现有逻辑 ...
    reward = project.complete()
    
    # 应用难度报酬倍率
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    reward *= config.get("project_reward_mult", 1.0)
    
    self.cash += reward
    # ...
```

### 4.3 薪资计算

```python
def get_agent_daily_salary(self) -> int:
    """计算每日总薪资"""
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    salary_mult = config.get("salary_mult", 1.0)
    return sum(int(a.salary * salary_mult) for a in self.agents)
```

### 4.4 设备购买

```python
def buy_equipment(self, equipment_name: str) -> dict:
    """购买设备"""
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    price_mult = config.get("equipment_price_mult", 1.0)
    
    base_price = self.EQUIPMENT_CONFIG.get(equipment_name, {}).get("cost", 0)
    price = int(base_price * price_mult)
    
    if self.cash < price:
        return {"success": False, "error": f"现金不足 (需要 ${price})"}
    
    # ...
```

### 4.5 品牌维护费

```python
def get_brand_daily_cost(self) -> float:
    """获取品牌日维护费"""
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    maintenance_mult = config.get("brand_maintenance_mult", 1.0)
    
    base_cost = self.BRAND_CONFIG.get(int(self.brand_level), self.BRAND_CONFIG[0])["daily_cost"]
    return base_cost * maintenance_mult
```

### 4.6 项目质量计算

```python
def calculate_quality(self, agents: List[Agent]) -> float:
    """计算项目质量"""
    # ... 现有逻辑 ...
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    quality_requirement = config.get("quality_requirement", 1.0)
    
    return max(0, min(100, base_quality / quality_requirement))
```

### 4.7 事件触发

```python
def trigger_random_event(self) -> Optional[GameEvent]:
    """触发随机事件"""
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    event_frequency = config.get("event_frequency", 1.0)
    
    if random.random() < 0.1 * event_frequency:  # 基础概率 10%
        return self.events[random.randint(0, len(self.events) - 1)]
    return None
```

### 4.8 项目难度

```python
def next_day(self) -> dict:
    """进入下一天"""
    # ... 项目进度推进 ...
    config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["normal"])
    difficulty_mult = config.get("project_difficulty_mult", 1.0)
    
    daily_progress = int(daily_progress * difficulty_mult)
    # ...
```

---

## 5. API 设计

| API | 方法 | 说明 |
|-----|------|------|
| `/api/difficulty/list` | GET | 获取所有难度模式配置 |
| `/api/difficulty/current` | GET | 获取当前游戏难度 |
| `/api/difficulty/set` | POST | 设置难度（仅新游戏前） |
| `/api/difficulty/custom` | POST | 设置自定义难度参数 |

---

## 6. UI 设计

### 6.1 难度选择页面

```
┌─────────────────────────────────────────────┐
│          🎮 AI 创业模拟器                   │
│                                             │
│        选择难度模式                          │
│                                             │
│  ┌─────────────┐ ┌─────────────┐           │
│  │ 🌟 简单模式  │ │ ⚖️ 普通模式  │           │
│  │             │ │             │           │
│  │ 初始资金     │ │ 初始资金     │           │
│  │ $100,000    │ │ $75,000     │           │
│  │             │ │             │           │
│  │ 项目报酬 1.3x│ │ 项目报酬 1.0x│           │
│  │ 薪资 0.8x   │ │ 薪资 1.0x   │           │
│  │             │ │             │           │
│  │ [开始游戏]   │ │ [开始游戏]   │           │
│  └─────────────┘ └─────────────┘           │
│                                             │
│  ┌─────────────┐ ┌─────────────┐           │
│  │ 🔥 困难模式  │ │ ⚙️ 自定义模式│           │
│  │             │ │             │           │
│  │ 初始资金     │ │ 初始资金     │           │
│  │ $25,000     │ │ [输入框]     │           │
│  │             │ │             │           │
│  │ 项目报酬 0.7x│ │ [滑块调整]   │           │
│  │ 薪资 1.3x   │ │             │           │
│  │             │ │             │           │
│  │ [开始游戏]   │ │ [开始游戏]   │           │
│  └─────────────┘ └─────────────┘           │
│                                             │
│  💡 提示：简单模式适合新手，困难模式         │
│     提供更高挑战性。                        │
└─────────────────────────────────────────────┘
```

### 6.2 自定义难度参数面板

```
┌─────────────────────────────────────────────┐
│ ⚙️ 自定义难度参数                            │
│                                             │
│ 初始资金: [$75,000]  [$10k - $500k]        │
│ 项目报酬倍率: [1.0x]  [0.5x - 2.0x]        │
│ 员工薪资倍率: [1.0x]  [0.5x - 2.0x]        │
│ 设备价格倍率: [1.0x]  [0.5x - 2.0x]        │
│ 品牌维护费倍率: [1.0x]  [0.5x - 2.0x]      │
│ 质量要求: [正常]  [宽松/正常/严格]          │
│ 事件频率: [正常]  [低/正常/高]              │
│ 项目难度: [正常]  [简单/正常/困难]          │
│                                             │
│                    [开始游戏]  [重置]        │
└─────────────────────────────────────────────┘
```

---

## 7. 存档集成

```python
# Company.to_dict() 新增
def to_dict(self) -> dict:
    return {
        # ... 现有字段 ...
        "difficulty": self.difficulty,
        "difficulty_settings": self.difficulty_settings,
    }

# Company.from_dict() 新增
@classmethod
def from_dict(cls, data: dict) -> "Company":
    company = cls()
    # ... 现有字段 ...
    company.difficulty = data.get("difficulty", "normal")
    company.difficulty_settings = data.get("difficulty_settings", {})
    return company
```

---

## 8. 开发顺序

| Sprint | 内容 | 工期 | 负责人 |
|--------|------|------|--------|
| 1 | 难度数据模型 + 配置 | 1 天 | 全栈开发 |
| 2 | 难度参数应用逻辑 | 2 天 | 全栈开发 |
| 3 | 难度选择 UI | 2 天 | 全栈开发 + 创意总监 |
| 4 | 自定义难度面板 | 1 天 | 全栈开发 |
| 5 | 测试 | 2 天 | 测试工程师 |

**总工期**: 8 天

---

## 9. 成功标准

- [ ] 4 种难度模式可切换
- [ ] 初始资金正确应用
- [ ] 项目报酬/薪资/设备价格/品牌维护费倍率正确
- [ ] 质量要求/事件频率/项目难度正确
- [ ] 自定义难度参数可调整
- [ ] 存档/读档后难度设置正确保存
- [ ] 所有难度模式通过测试

---

## 10. 风险清单

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 难度参数过多 | 玩家难以理解 | 提供难度说明 + 预设难度 |
| 自定义难度不平衡 | 游戏太简单或太难 | 设置参数范围限制 |
| 存档兼容性 | 旧存档无难度字段 | 默认使用 "normal" |

---

**文档引用**:
- `design/phase3-roadmap.md` — 整体路线图
- `design/phase3.5-difficulty-assets.md` — 创意资产包
