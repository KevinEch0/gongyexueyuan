
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map


# 创建数据库连接对象
db = SQLAlchemy()

def create_app(config_name):

    # 创建app实例
    app = Flask(__name__)

    # 必须先加载配置，再初始化插件
    from config import config_map
    app.config.from_object(config_map[config_name])
    
    # 关键修复：强制设置 JSON 编码器
    app.json.ensure_ascii = False  # 覆盖所有 JSON 响应
    

    # 加载配置信息
    Config = config_map.get(config_name)

    # 根据类来加载配置信息
    app.config.from_object(Config)

    # 创建数据库连接对象
    db.init_app(app)

    # 获取user蓝图对象
    from xueyuan1_0.user import user_bp
    # 注册蓝图对象
    app.register_blueprint(user_bp)

    # 获取menu蓝图对象
    from xueyuan1_0.menu import menu_bp
    # 注册蓝图对象
    app.register_blueprint(menu_bp)

    # 获取role蓝图对象
    from xueyuan1_0.role import role_bp
    # 注册蓝图对象
    app.register_blueprint(role_bp)

    # 返回app实例
    return app

