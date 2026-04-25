"""
难度系统 API 路由
"""

from flask import Blueprint, jsonify, request

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import get_current_game
from models.company import Company

bp = Blueprint("difficulty", __name__)


@bp.route("", methods=["GET"])
def get_difficulty():
    """获取当前难度配置"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    company = game.company
    config = company.get_difficulty_config()
    
    return jsonify({
        "difficulty": company.difficulty,
        "config": config,
    })


@bp.route("/<mode>", methods=["POST"])
def set_difficulty(mode: str):
    """设置难度 (新游戏时)"""
    if mode not in Company.DIFFICULTY_CONFIG and mode != "custom":
        return jsonify({"error": f"Invalid difficulty mode: {mode}"}), 400
    
    data = request.get_json() or {}
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    company = game.company
    company.difficulty = mode
    
    if mode == "custom":
        # 自定义难度参数
        company.difficulty_settings = {
            "initial_cash": data.get("initial_cash", 75000),
            "reward_multiplier": data.get("reward_multiplier", 1.0),
            "salary_multiplier": data.get("salary_multiplier", 1.0),
            "equipment_price_multiplier": data.get("equipment_price_multiplier", 1.0),
            "brand_maintenance_multiplier": data.get("brand_maintenance_multiplier", 1.0),
        }
    else:
        company.difficulty_settings = {}
    
    # 应用初始资金
    config = company.get_difficulty_config()
    company.cash = config.get("initial_cash", 75000)
    
    return jsonify({
        "success": True,
        "difficulty": company.difficulty,
        "cash": company.cash,
    })


@bp.route("/config", methods=["GET"])
def get_difficulty_config():
    """获取所有难度配置"""
    return jsonify({
        "difficulties": Company.DIFFICULTY_CONFIG,
    })
