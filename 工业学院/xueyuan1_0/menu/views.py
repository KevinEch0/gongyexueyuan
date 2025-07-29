# from flask import request

# from flask_restful import Resource

# from xueyuan1_0.menu import menu_api

# from xueyuan1_0 import models


# class Menus(Resource):
#     def get(self):
#         # 获取前端页面要求的数据类型,list tree
#         type_ = request.args.get('type_')
#         # 根据type_决定以什么结构返回数据
#         if type_ == 'tree':
#             # 通过模型获取数据
#             menu_list = models.Menu.query.filter(models.Menu.level == 1).all()
#             menu_data = []
#             # 遍历数据
#             for m in menu_list:
#                 menu_data.append(m.to_dict_tree())
#             return {'status': 200, 'msg': '获取菜单成功', 'data': menu_data}    
#         else:
#             # 通过模型获取数据
#             menu_list = models.Menu.query.filter(models.Menu.level != 0).all()
#             menu_data = []
#             # 遍历数据
#             for m in menu_list:
#                 menu_data.append(m.to_dict_list())
#             return {'status': 200, 'msg': '获取菜单成功', 'data': menu_data}    
# menu_api.add_resource(Menus, '/menus/')



from flask import request
from flask_restful import Resource
from xueyuan1_0.menu import menu_api
from xueyuan1_0 import models, db

class Menus(Resource):
    def get(self):
        # 1. 获取请求参数
        type_ = request.args.get('type_', 'list')  # 默认返回列表形式
        user_id = request.args.get('user_id')      # 必须传递的用户ID
        # print("GGG",user_id)

        # 2. 验证user_id
        if user_id not in ['1', '4']:
            return {'status': 400, 'msg': '无效的用户ID', 'data': None}

        try:
            # 3. 根据user_id决定查询方式
            if user_id == '4':  # 管理员返回全部菜单
                menu_query = db.session.query(models.Menu)
            else:  # 普通用户(user_id=1)
                # print(f"[权限] 普通用户(user_id={user_id})，查询角色关联菜单")
                user = db.session.query(models.User).get(user_id)
                if not user:
                    return {'status': 404, 'msg': '用户不存在', 'data': None}
                user.role_id=user_id
                # print(f"[用户角色] role_id={user.role_id}")
                
                # 关联表查询调试
                # print("\n[关联表查询] 准备查询 trm 表...")
                trm_query = db.session.query(models.trm).filter(
                    models.trm.c.role_id == user.role_id
                )
                # print(f"[SQL] trm表查询语句: {trm_query}")
                trm_records = trm_query.all()
                # print(f"[结果] 关联表记录数: {len(trm_records)}")
                # print(f"[详情] 关联的menu_id列表: {[r.menu_id for r in trm_records]}")

                menu_query = db.session.query(models.Menu).join(
                    models.trm,
                    models.Menu.id == models.trm.c.menu_id
                ).filter(
                    models.trm.c.role_id == user.role_id
                )
                # print(f"\n[最终SQL] 菜单查询语句: {menu_query}")

            # 4. 根据type_返回不同结构
            if type_ == 'tree':
                # 树形结构：查询一级菜单
                menus = menu_query.filter(models.Menu.level == 1).all()
                menu_data = [m.to_dict_tree() for m in menus]
            else:
                # 列表结构：查询所有非零级菜单
                menus = menu_query.filter(models.Menu.level != 0).all()
                menu_data = [m.to_dict_list() for m in menus]

            return {
                'status': 200,
                'msg': '获取菜单成功',
                'data': menu_data
            }

        except Exception as e:
            db.session.rollback()
            return {'status': 500, 'msg': f'服务器错误: {str(e)}', 'data': None}

menu_api.add_resource(Menus, '/menus/')


class Menus2(Resource):
    def get(self):
        # 获取前端页面要求的数据类型,list tree
        type_ = request.args.get('type_')
        # 根据type_决定以什么结构返回数据
        if type_ == 'tree':
            # 通过模型获取数据
            menu_list = models.Menu.query.filter(models.Menu.level == 1).all()
            menu_data = []
            # 遍历数据
            for m in menu_list:
                menu_data.append(m.to_dict_tree())
            return {'status': 200, 'msg': '获取菜单成功', 'data': menu_data}    
        else:
            # 通过模型获取数据
            menu_list = models.Menu.query.filter(models.Menu.level != 0).all()
            menu_data = []
            # 遍历数据
            for m in menu_list:
                menu_data.append(m.to_dict_list())
            return {'status': 200, 'msg': '获取菜单成功', 'data': menu_data}    
menu_api.add_resource(Menus2, '/menus2/')
