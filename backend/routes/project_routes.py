"""
项目相关 API 路由
"""

from flask import Blueprint, jsonify, request

from ..services import get_current_game

bp = Blueprint("project", __name__)


@bp.route("", methods=["GET"])
def list_projects():
    """列出项目"""
    status = request.args.get("status")
    game = get_current_game()
    projects = game.list_projects(status)
    return jsonify({"projects": projects})


@bp.route("/accept", methods=["POST"])
def accept_project():
    """接受项目"""
    data = request.get_json() or {}
    project_id = data.get("project_id")
    
    if not project_id:
        return jsonify({"error": "Project ID required"}), 400
    
    game = get_current_game()
    result = game.accept_project(project_id)
    
    return jsonify(result)


@bp.route("/assign", methods=["POST"])
def assign_agent():
    """分配 Agent 到项目"""
    data = request.get_json() or {}
    agent_id = data.get("agent_id")
    project_id = data.get("project_id")
    
    if not agent_id or not project_id:
        return jsonify({"error": "Agent ID and Project ID required"}), 400
    
    game = get_current_game()
    result = game.assign_agent(agent_id, project_id)
    
    return jsonify(result)


@bp.route("/complete", methods=["POST"])
def complete_project():
    """完成项目"""
    data = request.get_json() or {}
    project_id = data.get("project_id")
    
    if not project_id:
        return jsonify({"error": "Project ID required"}), 400
    
    game = get_current_game()
    result = game.complete_project(project_id)
    
    return jsonify(result)
