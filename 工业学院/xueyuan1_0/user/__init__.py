from flask import Blueprint
from flask_restful import Api

# 创建蓝图
user_bp = Blueprint('user', __name__,url_prefix='/user')

# 创建Api
user_api = Api(user_bp)

# 导入视图
from . import views