# Phase 3.3 公司成长系统 — 需求 Brief

**版本**: v1.0  
**日期**: 2026-04-23  
**产品经理**: 产品经理  
**状态**: 待开发

---

## 1. 范围

Phase 3.3 包含三个子系统：

| 系统 | 说明 | 优先级 |
|------|------|--------|
| 设备购买 | 一次性购买永久生效的被动加成设备 | P0 |
| 品牌建设 | 品牌等级影响报酬和项目质量，需要持续维护 | P1 |
| 投资融资 | 用股权换取现金，产生分红压力和控制权风险 | P2 |

**已有基础**：办公室升级（5 级）已在 Phase 3.1/3.2 实现，`Company.upgrade_office()` 和 API 完整可用，无需重复开发。

---

## 2. 设计决策（已确认）

| 决策点 | 结论 |
|--------|------|
| 加成叠加方式 | 加算，总加成上限 150%（2.5x） |
| 品牌维护费 | 按月扣除（每 30 天），数值 $500-$5000/天 量级 |
| 品牌衰减 | 每周结算一次，3 天宽限期 |
| 融资结局 | 股权 >50% → "创始人出局"叙事结局（非 Bad End） |
| 回购机制 | 支持用现金回购股权，估值 = `total_earnings × (1 + reputation × 0.2)` |
| 设备加成生效时机 | 进度加成在 `next_day()` 项目推进时生效，报酬加成在项目完成时生效 |
| 3.2 vs 3.3 | 先收口 3.2（团队羁绊），再启动 3.3 |

---

## 3. 子系统详细设计

### 3.1 设备购买系统

**数据模型**：
```python
# Company dataclass 新增
equipments: List[str] = field(default_factory=list)
```

**设备列表**：

| 设备 | 价格 | 效果 | 解锁条件 |
|------|------|------|---------|
| 高速网络 | $10,000 | 项目进度 +5% | 无 |
| 开发者工作站 | $25,000 | 程序员效率 +10% | 办公室 ≥2 级 |
| 云服务器集群 | $50,000 | 所有项目进度 +10% | 办公室 ≥3 级 |
| 测试实验室 | $35,000 | 项目质量 +5% | 办公室 ≥3 级 |
| AI 训练集群 | $150,000 | AI 项目报酬 +20% | 办公室 ≥4 级 |

**API**：
- `POST /api/company/buy-equipment` — 购买设备，请求体 `{ "equipment_name": "高速网络" }`
- `GET /api/company/equipments` — 获取已购买设备列表

**加成计算**：
```python
def get_equipment_bonus(company: Company) -> float:
    bonuses = {
        "高速网络": 0.05,
        "开发者工作站": 0.10,
        "云服务器集群": 0.10,
        "测试实验室": 0.05,
        "AI 训练集群": 0.20,
    }
    return sum(bonuses.get(e, 0) for e in company.equipments)
```

**进度加成生效位置**：`Company.next_day()` 中项目进度推进后应用  
**报酬加成生效位置**：`Company.complete_project()` 中报酬计算时应用

---

### 3.2 品牌建设系统

**数据模型**：
```python
# Company dataclass 新增
brand_level: float = 0.0          # 品牌等级 (0-5)
brand_warning_until: int = 0      # 品牌宽限期截止天数
```

**品牌等级表**：

| 等级 | 名称 | 日维护费 | 报酬倍率 | 好项目概率加成 |
|------|------|---------|---------|--------------|
| 0 | 无名小卒 | $0 | 1.0x | 0% |
| 1 | 地方知名 | $500 | 1.1x | 10% |
| 2 | 行业新锐 | $1,000 | 1.2x | 20% |
| 3 | 知名公司 | $2,000 | 1.3x | 30% |
| 4 | 行业巨头 | $3,500 | 1.5x | 40% |
| 5 | 科技帝国 | $5,000 | 2.0x | 50% |

**营销活动**：

| 活动 | 成本 | 品牌提升 |
|------|------|---------|
| 社交媒体推广 | $15,000 | +0.5 级 |
| 行业展会参展 | $30,000 | +1 级 |
| 电视广告 | $80,000 | +1.5 级 |
| 全球发布会 | $200,000 | +2 级 |

**衰减机制**：
- 每周（每 7 天）检查一次
- 检查维护费是否足够（7 天 × 日维护费）
- 不足则品牌等级 -0.5，给 3 天宽限期
- 宽限期后仍未续费则再 -0.5

**加成计算**：
```python
def get_brand_multiplier(company: Company) -> float:
    """品牌独立倍率（含 0.5 级支持）"""
    level = company.brand_level
    if level >= 5: return 2.0
    if level >= 4: return 1.5
    if level >= 3: return 1.3
    if level >= 2: return 1.2
    if level >= 1: return 1.1
    if level >= 0.5: return 1.05
    return 1.0
```

**API**：
- `POST /api/company/marketing` — 执行营销活动，请求体 `{ "campaign": "社交媒体推广" }`
- `GET /api/company/brand` — 获取品牌状态
- `POST /api/company/maintain-brand` — 续费维护，请求体 `{ "days": 30 }`

**维护费扣除位置**：`Company.next_day()` 中 `day % 30 == 0` 时扣除（月维护费 = 日维护费 × 30）

**衰减检查位置**：`Company.next_day()` 中 `day % 7 == 0` 时检查。付不起维护费 → 标记 `brand_warning_until = day + 3` → 到宽限期仍未续费 → 再扣 0.5 级

---

### 3.3 投资融资系统

**数据模型**：
```python
# Company dataclass 新增
equity_sold: float = 0.0              # 已出让股权比例 (0-1)
investors: List[dict] = field(default_factory=list)  # 投资者列表
dividend_accumulator: float = 0.0     # 分红累计器
last_dividend_day: int = 0            # 上次分红结算天数
```

**融资轮次**：

| 轮次 | 可融资金 | 出让股权 | 解锁条件 | 季度分红比例 |
|------|---------|---------|---------|------------|
| 种子轮 | $100,000 | 10% | 第 10 天 | 净利润的 5% |
| 天使轮 | $300,000 | 15% | 第 30 天，reputation ≥3.5 | 净利润的 8% |
| A 轮 | $800,000 | 20% | 第 60 天，reputation ≥4.0 | 净利润的 10% |
| B 轮 | $2,000,000 | 15% | 第 100 天，reputation ≥4.5 | 净利润的 12% |
| IPO | $5,000,000 | 10% | 第 150 天，reputation ≥4.8 | 净利润的 15% |

**分红计算**：
- 每天记录净利润（项目收入 - 工资 - 租金 - 维护费）
- 每 30 天结算一次，按总分红比例从现金中扣除
- 现金不足时从 `dividend_accumulator` 累计欠款
- 欠款超过 1 个月 → reputation -0.2

**回购机制**：
```python
def buyback_equity(company: Company, amount: float) -> dict:
    net_profit = max(company.total_earnings - company.total_expenses, 1)
    valuation = net_profit * (1 + company.reputation * 0.2)
    if valuation <= 0:
        return {"error": "Company has no valuation yet"}
    equity_bought = amount / valuation
    if equity_bought > company.equity_sold:
        equity_bought = company.equity_sold
    company.cash -= amount
    company.equity_sold -= equity_bought
    return {"success": True, "equity_bought": equity_bought, "remaining_equity": company.equity_sold}
```

**结局判定**：
- `equity_sold > 0.5` → 触发"创始人出局"叙事结局
- 结局画面显示：股权比例、最终得分、公司估值
- 不是 Bad End，是另一种故事线

**API**：
- `POST /api/company/funding` — 申请融资，请求体 `{ "round": "种子轮" }`
- `POST /api/company/buyback` — 回购股权，请求体 `{ "amount": 100000 }`
- `GET /api/company/funding` — 获取融资状态

**分红扣除位置**：`Company.next_day()` 中每 30 天结算

---

## 4. 总加成计算

```python
def get_total_project_multiplier(company: Company) -> float:
    """项目报酬总加成 = 品牌倍率 + 设备加成，上限 2.5x"""
    brand_base = {0: 1.0, 1: 1.1, 2: 1.2, 3: 1.3, 4: 1.5, 5: 2.0}.get(
        int(company.brand_level), 1.0
    )
    equipment_bonus = get_equipment_bonus(company)
    return min(brand_base + equipment_bonus, 2.5)
```

---

## 5. 开发顺序

1. **Sprint 0**: 收口 Phase 3.2（团队羁绊）— 2 天
2. **Sprint 1**: 设备系统 — 3 天
3. **Sprint 2**: 品牌系统 — 4 天
4. **Sprint 3**: 融资系统 — 5 天
5. **Sprint 4**: 集成测试 + 发布 — 2 天

**总工期**: 16 天（4/24 - 5/9）

---

## 6. 成功标准

- [ ] 5 种设备可购买，加成正确生效
- [ ] 品牌等级可提升/衰减/维护，加成正确计算
- [ ] 5 轮融资可触发，分红正确结算
- [ ] 回购机制正常工作
- [ ] 股权 >50% 触发叙事结局
- [ ] 总加成不超过 2.5x
- [ ] 所有系统通过集成测试
- [ ] 发布说明已输出

---

**附件**：
- `backend/models/company.py` — 现有数据模型基线
- `backend/routes/company_routes.py` — 现有 API 路由基线
- `backend/services/game_engine.py` — 核心引擎基线
