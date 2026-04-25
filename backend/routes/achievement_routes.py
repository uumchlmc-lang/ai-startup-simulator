"""
成就系统 API 路由
"""

from flask import Blueprint, jsonify, request

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import get_current_game
from services.achievement_engine import AchievementEngine

bp = Blueprint("achievement", __name__)
achievement_engine = AchievementEngine()


@bp.route("", methods=["GET"])
def get_achievements():
    """获取所有成就状态"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    achievements = achievement_engine.get_all_achievements(game.company)
    return jsonify({
        "achievements": achievements,
        "unlocked_count": len(game.company.achievements),
        "total_count": len(achievements),
    })


@bp.route("/unlocked", methods=["GET"])
def get_unlocked_achievements():
    """获取已解锁成就"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    unlocked = []
    for aid in game.company.achievements:
        achievement = achievement_engine.get_achievement(aid)
        if achievement:
            unlocked.append(achievement)
    
    return jsonify({"achievements": unlocked})


@bp.route("/progress/<achievement_id>", methods=["GET"])
def get_achievement_progress(achievement_id: str):
    """获取成就进度"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    progress = achievement_engine.get_progress(game.company, achievement_id)
    return jsonify(progress)


@bp.route("/check", methods=["POST"])
def check_achievements():
    """手动检查成就（通常自动触发）"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    new_unlocks = achievement_engine.check_all(game.company)
    
    return jsonify({
        "new_unlocks": new_unlocks,
        "total_unlocked": len(game.company.achievements),
    })
