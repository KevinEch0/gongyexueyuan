from flask import Blueprint
from flask_restful import Api


# 创建蓝图
role_bp = Blueprint('role', __name__)
role_api = Api(role_bp)



from . import views