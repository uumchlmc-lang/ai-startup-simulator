"""
Agent 相关 API 路由
"""

from flask import Blueprint, jsonify, request

from ..services import get_current_game

bp = Blueprint("agent", __name__)


@bp.route("", methods=["GET"])
def list_agents():
    """列出所有 Agent"""
    game = get_current_game()
    agents = game.list_agents()
    return jsonify({"agents": agents})


@bp.route("/hire", methods=["POST"])
def hire_agent():
    """雇佣 Agent"""
    data = request.get_json() or {}
    role = data.get("role", "初级程序员")
    name = data.get("name")
    
    game = get_current_game()
    result = game.hire_agent(role, name)
    
    return jsonify(result)


@bp.route("/fire", methods=["POST"])
def fire_agent():
    """解雇 Agent"""
    data = request.get_json() or {}
    agent_id = data.get("agent_id")
    
    if not agent_id:
        return jsonify({"error": "Agent ID required"}), 400
    
    game = get_current_game()
    result = game.fire_agent(agent_id)
    
    return jsonify(result)


@bp.route("/train", methods=["POST"])
def train_agent():
    """培训 Agent"""
    data = request.get_json() or {}
    agent_id = data.get("agent_id")
    
    if not agent_id:
        return jsonify({"error": "Agent ID required"}), 400
    
    game = get_current_game()
    result = game.train_agent(agent_id)
    
    return jsonify(result)
