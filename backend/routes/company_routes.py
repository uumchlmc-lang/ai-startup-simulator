"""
公司相关 API 路由
"""

from flask import Blueprint, jsonify, request

from ..services import get_current_game

bp = Blueprint("company", __name__)


@bp.route("", methods=["GET"])
def get_company():
    """获取公司信息"""
    game = get_current_game()
    return jsonify(game.get_company_status())


@bp.route("/rename", methods=["POST"])
def rename_company():
    """改名"""
    data = request.get_json() or {}
    new_name = data.get("new_name")
    
    if not new_name:
        return jsonify({"error": "Name required"}), 400
    
    game = get_current_game()
    result = game.rename_company(new_name)
    
    return jsonify(result)


@bp.route("/upgrade-office", methods=["POST"])
def upgrade_office():
    """升级办公室"""
    game = get_current_game()
    result = game.upgrade_office()
    
    return jsonify(result)


@bp.route("/research", methods=["POST"])
def research_technology():
    """研发科技"""
    data = request.get_json() or {}
    tech_name = data.get("tech_name")
    
    if not tech_name:
        return jsonify({"error": "Tech name required"}), 400
    
    game = get_current_game()
    result = game.research_technology(tech_name)
    
    return jsonify(result)
