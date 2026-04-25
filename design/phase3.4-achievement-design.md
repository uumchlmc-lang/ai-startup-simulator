# Phase 3.4 成就系统 — 技术设计文档

**版本**: v1.0  
**日期**: 2026-04-25  
**产品经理**: 产品经理  
**状态**: 待开发

---

## 1. 范围

Phase 3.4 包含两个子系统：

| 系统 | 说明 | 优先级 |
|------|------|--------|
| 成就系统 | 52 个成就，8 大分类，自动触发 | P0 |
| 排行榜系统 | 成就进度显示 + 解锁率 + 排行榜 | P1 |

**已有基础**：创意资产 `design/phase3.4-achievement-assets.md` 已产出 52 个成就的名称、描述、图标、触发条件。

---

## 2. 数据模型

```python
# Company dataclass 新增
achievements: List[str] = field(default_factory=list)  # 已解锁成就 ID 列表
achievement_progress: Dict[str, dict] = field(default_factory=dict)  # 成就进度追踪
```

**成就进度结构**：
```python
{
    "project_completed_10": {"current": 5, "target": 10, "unlocked": False},
    "agents_10": {"current": 8, "target": 10, "unlocked": False},
}
```

---

## 3. 成就分类与触发条件

### 3.1 成长成就 (10 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `project_completed_1` | 迈出第一步 | `projects_completed >= 1` | 项目完成时 |
| `project_completed_10` | 初出茅庐 | `projects_completed >= 10` | 项目完成时 |
| `project_completed_50` | 渐入佳境 | `projects_completed >= 50` | 项目完成时 |
| `project_completed_100` | 身经百战 | `projects_completed >= 100` | 项目完成时 |
| `day_100` | 创业老兵 | `day >= 100` | `next_day()` |
| `day_365` | 十年磨剑 | `day >= 365` | `next_day()` |
| `office_level_5` | 车库传奇 | `office_level >= 5` | 办公室升级时 |
| `reputation_5` | 名声大噪 | `reputation >= 5.0` | `next_day()` |
| `reputation_5_projects_100` | 行业标杆 | `reputation >= 5.0 && projects_completed >= 100` | `next_day()` |
| `day_730` | 百年老店 | `day >= 730` | `next_day()` |

### 3.2 项目成就 (8 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `quality_100` | 完美交付 | `project.quality == 100` | 项目完成时 |
| `early_complete` | 速战速决 | 提前 50%+ 时间完成 | 项目完成时 |
| `last_minute` | 压哨绝杀 | 截止前 1 天完成 | 项目完成时 |
| `all_project_types` | 全栈高手 | 完成全部 13 种类型 | 项目完成时 |
| `big_deal_500k` | 大单王 | `single_reward >= 500000` | 项目完成时 |
| `quality_90_50times` | 质量控 | 50 次质量 ≥ 90 | 项目完成时 |
| `failed_5` | 烂尾楼 | `projects_failed >= 5` | 项目失败时 |
| `comeback_10` | 逆风翻盘 | 失败后连续 10 次完成 | 项目完成时 |

### 3.3 团队成就 (7 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `agent_1` | 光杆司令 | `len(agents) >= 1` | 雇佣时 |
| `agent_10` | 十人团 | `len(agents) >= 10` | 雇佣时 |
| `agent_100` | 百人战队 | `len(agents) >= 100` | 雇佣时 |
| `level_1_to_10` | 伯乐 | 有员工从 Lv1 升到 Lv10 | 员工升级时 |
| `five_level_10` | 名师出高徒 | 5 名员工 Lv ≥ 10 | 员工升级时 |
| `no_resign_100` | 铁打的营盘 | 100 天无离职 | `next_day()` |
| `fired_10` | 铁石心肠 | `fired_count >= 10` | 解雇时 |

### 3.4 设备成就 (4 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `equipment_1` | 网速飞起 | `len(equipments) >= 1` | 购买设备时 |
| `equipment_5` | 装备齐全 | `len(equipments) >= 5` | 购买设备时 |
| `equipment_spent_200k` | 土豪公司 | `equipment_total_spent >= 200000` | 购买设备时 |
| `ai_cluster` | 极客天堂 | `"AI 训练集群" in equipments` | 购买设备时 |

### 3.5 品牌成就 (5 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `brand_1` | 小有名气 | `brand_level >= 1` | 品牌升级时 |
| `brand_2` | 行业新锐 | `brand_level >= 2` | 品牌升级时 |
| `brand_3` | 行业焦点 | `brand_level >= 3` | 品牌升级时 |
| `brand_4` | 行业巨头 | `brand_level >= 4` | 品牌升级时 |
| `brand_5` | 科技帝国 | `brand_level >= 5` | 品牌升级时 |

### 3.6 融资成就 (7 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `funding_1` | 第一桶金 | `len(investors) >= 1` | 融资时 |
| `funding_angel` | 资本宠儿 | `"天使轮" in rounds` | 融资时 |
| `funding_a` | 资本玩家 | `"A 轮" in rounds` | 融资时 |
| `funding_ipo` | 敲钟时刻 | `"IPO" in rounds` | 融资时 |
| `buyback_all` | 东山再起 | `equity_sold == 0 && ever_had_equity` | 回购时 |
| `ipo_majority` | 上市敲钟 | `IPO && equity_sold < 0.5` | 融资时 |
| `founder_out` | 创始人出局 | `equity_sold > 0.5` | 融资时 |

### 3.7 财务成就 (5 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `earnings_100k` | 第一桶金 | `total_earnings >= 100000` | `next_day()` |
| `earnings_1m` | 百万富翁 | `total_earnings >= 1000000` | `next_day()` |
| `earnings_10m` | 千万帝国 | `total_earnings >= 10000000` | `next_day()` |
| `profitable_30` | 精打细算 | 30 天连续盈利 | `next_day()` |
| `bankruptcy_comeback` | 破产边缘 | `cash < -40000` 后 `cash > 0` | `next_day()` |

### 3.8 隐藏成就 (6 个)

| ID | 名称 | 触发条件 | 检查时机 |
|----|------|---------|---------|
| `consecutive_7` | 加班狂魔 | 连续 7 天执行 | `next_day()` |
| `idle_5` | 选择困难 | 5 天不接单 | `next_day()` |
| `lone_wolf` | 独狼 | 1 员工 + 50 天 | `next_day()` |
| `no_funding` | 氪金玩家 | 胜利时 `equity_sold == 0` | 游戏结束时 |
| `all_marketing` | 社交通 | 4 种营销活动都执行过 | 营销时 |
| `easter_42` | 彩蛋：42 | 第 42 天完成项目 | 项目完成时 |

---

## 4. 成就检查引擎

```python
class AchievementEngine:
    """成就检查引擎"""
    
    def __init__(self, company: Company):
        self.company = company
    
    def check_all(self) -> List[str]:
        """检查所有成就，返回新解锁的成就 ID 列表"""
        newly_unlocked = []
        
        for achievement_id, config in ACHIEVEMENTS.items():
            if achievement_id in self.company.achievements:
                continue  # 已解锁，跳过
            
            if config["check"](self.company):
                self.company.achievements.append(achievement_id)
                newly_unlocked.append(achievement_id)
        
        return newly_unlocked
    
    def check_on_project_complete(self, project: Project) -> List[str]:
        """项目完成时检查"""
        newly_unlocked = []
        
        for achievement_id, config in ACHIEVEMENTS.items():
            if achievement_id in self.company.achievements:
                continue
            if config.get("trigger") != "project_complete":
                continue
            if config["check"](self.company, project):
                self.company.achievements.append(achievement_id)
                newly_unlocked.append(achievement_id)
        
        return newly_unlocked
```

---

## 5. 排行榜系统

### 5.1 数据模型

```python
# Company dataclass 新增
achievement_unlock_rate: float = 0.0  # 解锁率 (0-100)
```

### 5.2 排行榜 API

| API | 方法 | 说明 |
|-----|------|------|
| `/api/achievements` | GET | 获取所有成就列表 + 解锁状态 |
| `/api/achievements/stats` | GET | 获取成就统计（解锁数/总数/解锁率） |
| `/api/achievements/unlock/{id}` | GET | 获取单个成就详情 |

### 5.3 排行榜 UI 布局

```
┌─────────────────────────────────────────────┐
│ 🏆 成就排行榜                               │
│                                             │
│ 已解锁: 12 / 52    解锁率: 23%             │
│                                             │
│ ┌─ 成长成就 ──────────────────────────────┐ │
│ │ ✅ 迈出第一步    🎯  第 3 天解锁        │ │
│ │ ✅ 初出茅庐      🌱  第 15 天解锁       │ │
│ │ 🔒 渐入佳境      🌿  5/50 项目          │ │
│ │ 🔒 身经百战      🔥  未解锁             │ │
│ │ ...                                     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ ┌─ 项目成就 ──────────────────────────────┐ │
│ │ ✅ 完美交付      💎  第 20 天解锁       │ │
│ │ 🔒 速战速决      ⚡  未解锁             │ │
│ │ ...                                     │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ [分类筛选] 全部 | 成长 | 项目 | 团队 | ...  │
└─────────────────────────────────────────────┘
```

---

## 6. 存档集成

```python
# Company.to_dict() 新增
def to_dict(self) -> dict:
    return {
        # ... 现有字段 ...
        "achievements": self.achievements,
        "achievement_progress": self.achievement_progress,
    }

# Company.from_dict() 新增
@classmethod
def from_dict(cls, data: dict) -> "Company":
    company = cls()
    # ... 现有字段 ...
    company.achievements = data.get("achievements", [])
    company.achievement_progress = data.get("achievement_progress", {})
    return company
```

---

## 7. 开发顺序

| Sprint | 内容 | 工期 | 负责人 |
|--------|------|------|--------|
| 1 | 成就数据模型 + 检查引擎 | 2 天 | 全栈开发 |
| 2 | 52 个成就触发逻辑 | 3 天 | 全栈开发 |
| 3 | 排行榜 API + UI | 2 天 | 全栈开发 + 创意总监 |
| 4 | 成就通知系统 | 1 天 | 全栈开发 |
| 5 | 测试 | 2 天 | 测试工程师 |

**总工期**: 10 天

---

## 8. 成功标准

- [ ] 52 个成就可触发
- [ ] 成就解锁时显示通知
- [ ] 排行榜显示解锁率
- [ ] 存档/读档后成就正确保存
- [ ] 隐藏成就不在列表中显示（或显示为"???"）
- [ ] 所有成就通过测试

---

## 9. 风险清单

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 成就触发时机复杂 | 可能漏触发 | 每个成就明确检查时机 |
| 隐藏成就泄露 | 破坏惊喜感 | 未解锁时显示"???" |
| 成就进度追踪性能 | 大量成就检查可能慢 | 只在相关事件时检查，非每次 next_day |

---

**文档引用**:
- `design/phase3.4-achievement-assets.md` — 52 个成就创意资产
- `design/phase3-roadmap.md` — 整体路线图
