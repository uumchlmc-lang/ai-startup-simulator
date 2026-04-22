# AI 创业模拟器 - 技术架构设计

**版本**: 1.0  
**架构师**: 技术总监  
**日期**: 2026-04-22

---

## 1. 技术选型

### 1.1 后端
| 组件 | 技术 | 理由 |
|------|------|------|
| 语言 | Python 3.11 | 开发效率高，小 K 熟悉 |
| 框架 | Flask | 轻量，适合快速原型 |
| 数据库 | SQLite | 无需部署，单文件 |
| 存储 | JSON | 存档格式，易读 |

### 1.2 前端
| 组件 | 技术 | 理由 |
|------|------|------|
| 语言 | HTML/CSS/JS | 浏览器原生支持 |
| UI 库 | 原生 JS | 简单，无需构建 |
| 图表 | Chart.js | 轻量，易用 |
| 图标 | Emoji | 免费，无需美术 |

### 1.3 部署
| 平台 | 方式 | 成本 |
|------|------|------|
| 本地 | Python 直接运行 | 免费 |
| Web | Vercel/Netlify | 免费 |
| Steam | Electron 打包 | $100 (上架费) |

---

## 2. 系统架构

```
┌─────────────────────────────────────────────────┐
│                   前端 (HTML/JS)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  办公室  │  │  项目看板  │  │   状态   │      │
│  │  视图    │  │  视图    │  │   面板   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
                        ↕ API (JSON)
┌─────────────────────────────────────────────────┐
│                 后端 (Python/Flask)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ 游戏逻辑  │  │  事件系统 │  │  存档系统 │      │
│  │  引擎    │  │          │  │          │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Agent 系统│  │ 项目系统  │  │ 财务系统  │      │
│  │          │  │          │  │          │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────┐
│                   数据层                         │
│  ┌──────────┐  ┌──────────┐                     │
│  │ SQLite   │  │ JSON     │                     │
│  │ 数据库   │  │ 存档文件  │                     │
│  └──────────┘  └──────────┘                     │
└─────────────────────────────────────────────────┘
```

---

## 3. 数据模型

### 3.1 公司 (Company)
```python
class Company:
    id: str                    # 公司 ID
    name: str                  # 公司名称
    cash: float                # 现金
    reputation: float          # 口碑 (0-5)
    day: int                   # 游戏天数
    office_level: int          # 办公室等级 (1-5)
    agents: List[Agent]        # Agent 列表
    projects: List[Project]    # 项目列表
    technologies: List[str]    # 已研发科技
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
```

### 3.2 Agent
```python
class Agent:
    id: str                    # Agent ID
    name: str                  # 姓名
    role: str                  # 角色 (程序员/设计师/...)
    level: int                 # 等级 (1-5)
    efficiency: int            # 效率 (0-100)
    creativity: int            # 创造力 (0-100)
    stability: int             # 稳定性 (0-100)
    satisfaction: int          # 满意度 (0-100)
    salary: int                # 薪资/天
    hired_at: datetime         # 雇佣时间
    status: str                # 状态 (工作中/请假/离职)
```

### 3.3 项目 (Project)
```python
class Project:
    id: str                    # 项目 ID
    name: str                  # 项目名称
    type: str                  # 类型 (网站/App/AI/...)
    difficulty: int            # 难度 (1-5)
    deadline: int              # 截止日期 (天数)
    reward: float              # 报酬
    progress: int              # 进度 (0-100)
    quality: int               # 质量 (0-100)
    status: str                # 状态 (进行中/已完成/失败)
    assigned_agents: List[str] # 分配的 Agent ID
    client_name: str           # 客户名称
    created_at: datetime       # 创建时间
```

### 3.4 事件 (Event)
```python
class Event:
    id: str                    # 事件 ID
    type: str                  # 类型 (positive/negative)
    name: str                  # 事件名称
    description: str           # 事件描述
    impact: dict               # 影响 (cash/reputation/...)
    triggered_at: datetime     # 触发时间
    duration: int              # 持续天数 (0=立即)
```

---

## 4. API 设计

### 4.1 公司相关
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/company | 获取公司信息 |
| POST | /api/company/rename | 改名 |
| GET | /api/company/status | 获取状态报告 |

### 4.2 Agent 相关
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/agents | 获取所有 Agent |
| POST | /api/agents/hire | 雇佣 Agent |
| POST | /api/agents/fire | 解雇 Agent |
| POST | /api/agents/train | 培训 Agent |

### 4.3 项目相关
| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/projects | 获取所有项目 |
| POST | /api/projects/accept | 接受项目 |
| POST | /api/projects/assign | 分配 Agent |
| POST | /api/projects/complete | 完成项目 |

### 4.4 游戏控制
| 方法 | 路径 | 描述 |
|------|------|------|
| POST | /api/game/next-day | 进入下一天 |
| POST | /api/game/save | 保存游戏 |
| POST | /api/game/load | 加载游戏 |
| GET | /api/game/events | 获取事件 |

---

## 5. 核心算法

### 5.1 项目进度计算
```python
def calculate_project_progress(project, agents):
    """
    计算项目每日进度
    """
    base_efficiency = sum(agent.efficiency for agent in agents)
    
    # 难度惩罚
    difficulty_penalty = 1.0 - (project.difficulty - 1) * 0.1
    
    # 科技加成
    tech_bonus = 1.0
    if '代码生成器' in company.technologies:
        tech_bonus += 0.3
    
    # 最终进度
    daily_progress = base_efficiency * difficulty_penalty * tech_bonus
    
    return min(daily_progress, 100)  # 最多 100%
```

### 5.2 项目质量计算
```python
def calculate_project_quality(project, agents):
    """
    计算项目交付质量
    """
    avg_creativity = sum(agent.creativity for agent in agents) / len(agents)
    avg_stability = sum(agent.stability for agent in agents) / len(agents)
    
    # 时间压力影响
    time_pressure = project.deadline / max(project.deadline, 1)
    
    # 质量分数
    quality = (avg_creativity * 0.6 + avg_stability * 0.4) * time_pressure
    
    return min(quality, 100)
```

### 5.3 事件触发
```python
def trigger_event(company):
    """
    随机触发事件
    """
    roll = random.random()
    
    if roll < 0.30:  # 30% 正面事件
        event = random.choice(POSITIVE_EVENTS)
    elif roll < 0.50:  # 20% 负面事件
        event = random.choice(NEGATIVE_EVENTS)
    else:
        return None  # 无事件
    
    return event
```

---

## 6. 文件结构

```
ai-startup-simulator/
├── backend/
│   ├── app.py                 # Flask 应用入口
│   ├── models/
│   │   ├── company.py         # 公司模型
│   │   ├── agent.py           # Agent 模型
│   │   ├── project.py         # 项目模型
│   │   └── event.py           # 事件模型
│   ├── services/
│   │   ├── game_engine.py     # 游戏引擎
│   │   ├── event_system.py    # 事件系统
│   │   └── save_system.py     # 存档系统
│   ├── routes/
│   │   ├── company_routes.py  # 公司 API
│   │   ├── agent_routes.py    # Agent API
│   │   └── project_routes.py  # 项目 API
│   └── config.py              # 配置文件
│
├── frontend/
│   ├── index.html             # 主页面
│   ├── css/
│   │   └── style.css          # 样式表
│   ├── js/
│   │   ├── app.js             # 应用入口
│   │   ├── components/        # UI 组件
│   │   └── api.js             # API 调用
│   └── assets/                # 资源文件
│
├── data/
│   ├── saves/                 # 存档目录
│   └── config.json            # 游戏配置
│
├── tests/
│   ├── test_models.py         # 模型测试
│   ├── test_engine.py         # 引擎测试
│   └── test_api.py            # API 测试
│
├── requirements.txt           # Python 依赖
├── package.json               # Node 依赖
└── README.md                  # 项目说明
```

---

## 7. 开发计划

### Phase 1: 后端核心 (3 天)
```
Day 1: 数据模型 + 数据库
Day 2: 游戏引擎 + 事件系统
Day 3: API 接口 + 测试
```

### Phase 2: 前端界面 (3 天)
```
Day 4: HTML 结构 + CSS 样式
Day 5: JS 交互 + API 调用
Day 6: UI 优化 + 动画
```

### Phase 3: 集成测试 (2 天)
```
Day 7: 前后端联调
Day 8: Bug 修复 + 优化
```

---

## 8. 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|
| Flask 性能不足 | 中 | 低 | 优化查询，加缓存 |
| SQLite 并发问题 | 低 | 低 | 单用户，无并发 |
| 前端兼容性问题 | 中 | 中 | 测试主流浏览器 |
| 存档损坏 | 高 | 低 | 多备份，校验和 |

---

## 9. 代码规范

### Python
- 遵循 PEP 8
- 类型注解
- 文档字符串
- 单元测试覆盖率 > 80%

### JavaScript
- ES6+ 语法
- 模块化
- 错误处理
- 注释清晰

---

**审批状态**: 待评审  
**下次更新**: 开发完成后
