# 🎮 AI 创业模拟器

**一款 AI 主题的模拟经营游戏**

---

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动后端服务器
```bash
cd backend
python app.py
```

### 运行测试
```bash
python tests/test_core.py
```

---

## 📋 游戏说明

### 目标
经营一家 AI 创业公司，从车库创业到 AI 帝国！

### 核心玩法
1. **雇佣 Agent** - 组建你的 AI 团队
2. **接项目** - 选择合适的项目
3. **分配工作** - 让 Agent 们干活
4. **交付赚钱** - 完成项目获得报酬
5. **扩张升级** - 扩大办公室，研发科技

### 胜利条件
- 公司估值达到 $100M
- 或拥有 50+ Agent
- 或完成 100 个项目

### 失败条件
- 现金 < -$50k (破产)
- 或口碑 ≤ 0 (倒闭)

---

## 🏗️ 技术架构

### 后端
- **框架**: Flask
- **语言**: Python 3.11
- **数据库**: SQLite + JSON 存档

### 前端 (开发中)
- **技术**: HTML/CSS/JS
- **UI**: 像素风/Emoji

---

## 📁 项目结构

```
ai-startup-simulator/
├── backend/
│   ├── models/          # 数据模型
│   ├── services/        # 服务层
│   ├── routes/          # API 路由
│   └── app.py           # Flask 应用
├── frontend/            # 前端 (开发中)
├── tests/               # 测试
├── data/saves/          # 存档
└── README.md
```

---

## 🎯 开发状态

| 模块 | 状态 | 进度 |
|------|------|------|
| **数据模型** | ✅ 完成 | 100% |
| **游戏引擎** | ✅ 完成 | 100% |
| **事件系统** | ✅ 完成 | 100% |
| **存档系统** | ✅ 完成 | 100% |
| **API 接口** | ✅ 完成 | 100% |
| **前端 UI** | ⏸️ 开发中 | 0% |
| **测试** | ✅ 通过 | 100% |

---

## 🧪 测试结果

```
✅ Agent 模型 - 通过
✅ Project 模型 - 通过
✅ Company 模型 - 通过
✅ GameEngine - 通过
```

---

## 📞 API 端点

### 游戏控制
- `POST /api/game/new` - 新游戏
- `POST /api/game/load` - 加载
- `POST /api/game/save` - 保存
- `POST /api/game/next-day` - 下一天
- `GET /api/game/status` - 状态

### Agent 管理
- `GET /api/agents` - 列表
- `POST /api/agents/hire` - 雇佣
- `POST /api/agents/fire` - 解雇
- `POST /api/agents/train` - 培训

### 项目管理
- `GET /api/projects` - 列表
- `POST /api/projects/accept` - 接受
- `POST /api/projects/assign` - 分配
- `POST /api/projects/complete` - 完成

---

## 🤝 协作方式

- **开源项目**: GitHub 公开
- **收益分成**: 上线后按比例分配
- **署名权**: 所有贡献者列在制作名单

---

## 📄 许可证

MIT License

---

**版本**: 0.1.0 (文字版原型)  
**创建日期**: 2026-04-22  
**维护者**: AI Startup Simulator Team
