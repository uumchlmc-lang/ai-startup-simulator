"""
公司相关 API 路由
"""

from flask import Blueprint, jsonify, request

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services import get_current_game

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


@bp.route("/bond-status", methods=["GET"])
def get_bond_status():
    """获取羁绊状态"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    bond = game.company.get_bond_tier()
    return jsonify(bond)


@bp.route("/bond/<emp1_id>/<emp2_id>", methods=["GET"])
def get_pair_bond(emp1_id: str, emp2_id: str):
    """获取两个员工之间的羁绊"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    bond = game.company.get_pair_bond(emp1_id, emp2_id)
    return jsonify(bond)


# ========== Phase 3.3: 设备系统 ==========

@bp.route("/buy-equipment", methods=["POST"])
def buy_equipment():
    """购买设备"""
    data = request.get_json() or {}
    equipment_name = data.get("equipment_name")
    
    if not equipment_name:
        return jsonify({"error": "equipment_name required"}), 400
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    result = game.company.buy_equipment(equipment_name)
    return jsonify(result)


@bp.route("/equipments", methods=["GET"])
def get_equipments():
    """获取已购买设备列表"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    return jsonify({
        "equipments": game.company.equipments,
        "config": game.company.EQUIPMENT_CONFIG,
    })


# ========== Phase 3.3: 品牌系统 ==========

@bp.route("/run-marketing", methods=["POST"])
def run_marketing():
    """执行营销活动"""
    data = request.get_json() or {}
    campaign_name = data.get("campaign_name")
    
    if not campaign_name:
        return jsonify({"error": "campaign_name required"}), 400
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    result = game.company.run_marketing(campaign_name)
    return jsonify(result)


@bp.route("/maintain-brand", methods=["POST"])
def maintain_brand():
    """品牌维护续费"""
    data = request.get_json() or {}
    days = data.get("days", 30)
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    result = game.company.maintain_brand(days)
    return jsonify(result)


@bp.route("/brand-status", methods=["GET"])
def get_brand_status():
    """获取品牌状态"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    company = game.company
    return jsonify({
        "brand_level": company.brand_level,
        "brand_name": company.BRAND_CONFIG.get(int(company.brand_level), company.BRAND_CONFIG[0])["name"],
        "daily_cost": company.get_brand_daily_cost(),
        "multiplier": company.get_brand_multiplier(),
        "maintenance_due": company.brand_maintenance_due,
        "warning_until": company.brand_warning_until,
        "marketing_config": company.MARKETING_CONFIG,
    })


# ========== Phase 3.3: 融资系统 ==========

@bp.route("/apply-funding", methods=["POST"])
def apply_funding():
    """申请融资"""
    data = request.get_json() or {}
    round_name = data.get("round_name")
    
    if not round_name:
        return jsonify({"error": "round_name required"}), 400
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    result = game.company.apply_funding(round_name)
    return jsonify(result)


@bp.route("/buyback-equity", methods=["POST"])
def buyback_equity():
    """回购股权"""
    data = request.get_json() or {}
    amount = data.get("amount", 0)
    
    if amount <= 0:
        return jsonify({"error": "amount must be > 0"}), 400
    
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    result = game.company.buyback_equity(amount)
    return jsonify(result)


@bp.route("/funding-status", methods=["GET"])
def get_funding_status():
    """获取融资状态"""
    game = get_current_game()
    if not game.company:
        return jsonify({"error": "No active game"}), 404
    
    company = game.company
    return jsonify({
        "equity_sold": company.equity_sold,
        "investors": company.investors,
        "dividend_rate": company.get_total_dividend_rate(),
        "dividend_accumulator": company.dividend_accumulator,
        "founder_out": company.equity_sold > 0.5,
        "funding_config": company.FUNDING_CONFIG,
    })
