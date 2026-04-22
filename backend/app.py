"""
AI 创业模拟器 - Flask 应用入口
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from .services import get_current_game, reset_game
from .routes import company_routes, agent_routes, project_routes


def create_app(config: dict = None):
    """创建 Flask 应用"""
    
    app = Flask(__name__)
    
    # 配置
    if config:
        app.config.update(config)
    
    # 启用 CORS
    CORS(app)
    
    # 注册蓝图
    app.register_blueprint(company_routes.bp, url_prefix="/api/company")
    app.register_blueprint(agent_routes.bp, url_prefix="/api/agents")
    app.register_blueprint(project_routes.bp, url_prefix="/api/projects")
    
    # 根路由
    @app.route("/")
    def index():
        return jsonify({
            "name": "AI Startup Simulator API",
            "version": "1.0.0",
            "status": "running",
        })
    
    # 游戏控制
    @app.route("/api/game/new", methods=["POST"])
    def new_game():
        """新游戏"""
        data = request.get_json() or {}
        company_name = data.get("company_name", "AI 创业公司")
        
        game = reset_game()
        company = game.new_game(company_name)
        
        return jsonify({
            "success": True,
            "company": company.to_dict(),
        })
    
    @app.route("/api/game/load", methods=["POST"])
    def load_game():
        """加载游戏"""
        data = request.get_json() or {}
        save_name = data.get("save_name", "autosave")
        
        game = get_current_game()
        company = game.load_game(save_name)
        
        if company:
            return jsonify({
                "success": True,
                "company": company.to_dict(),
            })
        else:
            return jsonify({
                "success": False,
                "error": "Save not found",
            }), 404
    
    @app.route("/api/game/save", methods=["POST"])
    def save_game():
        """保存游戏"""
        data = request.get_json() or {}
        save_name = data.get("save_name", "autosave")
        
        game = get_current_game()
        success = game.save_game(save_name)
        
        return jsonify({
            "success": success,
        })
    
    @app.route("/api/game/next-day", methods=["POST"])
    def next_day():
        """下一天"""
        game = get_current_game()
        result = game.next_day()
        
        return jsonify(result)
    
    @app.route("/api/game/status", methods=["GET"])
    def game_status():
        """游戏状态"""
        game = get_current_game()
        return jsonify(game.get_company_status())
    
    @app.route("/api/game/actions", methods=["GET"])
    def available_actions():
        """可用操作"""
        game = get_current_game()
        return jsonify({
            "actions": game.get_available_actions(),
        })
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not found",
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error",
        }), 500
    
    return app


# 开发服务器
if __name__ == "__main__":
    app = create_app({
        "DEBUG": True,
    })
    app.run(host="0.0.0.0", port=5000, debug=True)
