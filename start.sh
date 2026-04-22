#!/bin/bash
# AI 创业模拟器 - 启动脚本

echo "🎮 AI 创业模拟器 - 后端服务器"
echo "================================"
echo ""

# 检查依赖
echo "检查依赖..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask 未安装，正在安装..."
    pip3 install flask flask-cors
fi

echo "✅ 依赖检查完成"
echo ""

# 启动服务器
echo "启动服务器..."
echo "访问地址：http://localhost:5000"
echo ""

cd "$(dirname "$0")/backend"
python3 app.py
