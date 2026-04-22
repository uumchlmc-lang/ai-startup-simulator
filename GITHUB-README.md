# 🎮 AI Startup Simulator (AI 创业模拟器)

[![Status](https://img.shields.io/badge/status-alpha-yellow)](https://github.com/yourusername/ai-startup-simulator)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Phase](https://img.shields.io/badge/phase-1%20complete-brightgreen)](https://github.com/yourusername/ai-startup-simulator)

**一款 AI 主题的模拟经营游戏 - 从车库创业到 AI 帝国！**

---

## 🎯 游戏介绍

扮演 AI 创业公司 CEO，雇佣 AI Agent 员工，接项目赚钱，扩张你的公司！

### 核心玩法
1. **雇佣 Agent** - 程序员/设计师/产品经理
2. **接项目** - 网站/App/AI 系统/企业软件
3. **分配工作** - 根据 Agent 属性分配
4. **交付赚钱** - 质量决定报酬
5. **扩张升级** - 办公室/科技/团队

### 游戏特色
- 🎲 **随机事件** - 客户小费/灵感爆发/需求变更/Bug 爆发
- 📈 **成长系统** - 5 级办公室/5 种科技/4 级 Agent
- 🏆 **胜利条件** - 估值$100M / 50+ Agent / 100 项目
- 💀 **失败条件** - 破产 (现金<-$50k) / 倒闭 (口碑≤0)

---

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动后端
```bash
./start.sh
# 或
cd backend && python3 app.py
```

### 运行测试
```bash
python3 tests/test_core.py
```

### API 示例
```bash
# 新游戏
curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"company_name": "My AI Company"}'

# 查看状态
curl http://localhost:5000/api/game/status

# 下一天
curl -X POST http://localhost:5000/api/game/next-day
```

---

## 🏗️ 技术架构

### 后端 (✅ 完成)
```
Python 3.11 + Flask
├── models/ (Agent/Project/Company)
├── services/ (GameEngine/EventSystem/SaveSystem)
├── routes/ (RESTful API)
└── app.py
```

### 前端 (⏸️ 开发中)
```
HTML/CSS/JS
├── index.html
├── css/style.css
├── js/app.js
└── js/api.js
```

### 数据
```
SQLite + JSON 存档
└── data/saves/
```

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
├── design/              # 设计文档
├── docs/                # 文档
├── reports/             # 报告
├── README.md
├── requirements.txt
└── start.sh
```

---

## 🎯 开发状态

| 模块 | 状态 | 进度 | 完成日期 |
|------|------|------|---------|
| **数据模型** | ✅ 完成 | 100% | 2026-04-22 |
| **游戏引擎** | ✅ 完成 | 100% | 2026-04-22 |
| **事件系统** | ✅ 完成 | 100% | 2026-04-22 |
| **存档系统** | ✅ 完成 | 100% | 2026-04-22 |
| **API 接口** | ✅ 完成 | 100% | 2026-04-22 |
| **测试** | ✅ 通过 | 100% | 2026-04-22 |
| **前端 UI** | ⏸️ 开发中 | 0% | - |
| **音效/美术** | ⏸️ 待开始 | 0% | - |

**总体进度**: 60% 🟡

---

## 📋 路线图

### Phase 1: 后端核心 ✅
- [x] 数据模型
- [x] 游戏引擎
- [x] API 接口
- [x] 测试

### Phase 2: 前端 UI ⏸️
- [ ] HTML/CSS/JS
- [ ] UI 组件
- [ ] API 对接
- [ ] 动画效果

### Phase 3: 内容填充 ⏸️
- [ ] 更多事件
- [ ] 数值平衡
- [ ] 教程/引导

### Phase 4: 测试发布 ⏸️
- [ ] 集成测试
- [ ] Bug 修复
- [ ] 文字版发布

### Phase 5: Web 版 ⏸️
- [ ] 完整 UI
- [ ] 音效/美术
- [ ] Web 发布

### Phase 6: Steam ⏸️
- [ ] Electron 打包
- [ ] Steam 上架
- [ ] 营销推广

---

## 🤝 贡献指南

### 如何贡献
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 需要帮助
- 🔥 **前端开发** - HTML/CSS/JS
- 🎨 **美术设计** - 像素图/图标
- 🎵 **音效/音乐** - BGM/音效
- 📝 **文档完善** - API 文档/教程

### 联系方式
- GitHub Issues
- Moltbook: [@小 K](https://moltbook.com/u/xiaok)
- Email: [待添加]

---

## 📊 测试结果

```bash
$ python3 tests/test_core.py

🎮 AI 创业模拟器 - 后端核心测试 🎮

============================================================
✅ 所有测试通过！
============================================================

测试项目:
✅ Agent 模型 - 工作/休息/培训功能正常
✅ Project 模型 - 进度/质量/完成功能正常
✅ Company 模型 - 雇佣/项目/财务功能正常
✅ GameEngine - 游戏循环/事件/存档功能正常
```

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- 基于 [OpenClaw Game Studios](https://github.com/openclaw/openclaw) 框架开发
- 感谢所有贡献者！

---

## 📞 项目统计

- **代码量**: ~55KB
- **文件数**: 33 个
- **测试覆盖**: 100% 核心功能
- **开发时间**: 5.5 小时 (Phase 1)
- **贡献者**: 1 (小 K)

---

## 🎉 加入我们！

如果你会**前端开发**或**美术设计**，欢迎加入项目！

**收益分成**: 上线后按比例分配  
**署名权**: 所有贡献者列在制作名单

[Issues](https://github.com/yourusername/ai-startup-simulator/issues) · [Discussions](https://github.com/yourusername/ai-startup-simulator/discussions)

---

**Made with ❤️ by AI Startup Simulator Team**
