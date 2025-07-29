from xueyuan1_0.user import user_bp, user_api

from flask import request

from flask_restful import Resource,reqparse

from xueyuan1_0 import models ,db

from xueyuan1_0.utils.token import generate_token,virify_token,login_required

# 创建视图
@user_bp.route('/')
def index():
    return 'Hello World!'

# 登录功能
# @user_bp.route('/login/', methods=['POST'])
# def login():
#     # 获取用户名
#     # name = request.form.get('name')  # content-type: application/x-www-form-urlencoded
#     name = request.get_json().get('name')  # content-type: application/json
#     # 获取密码
#     pwd = request.get_json().get('pwd')
#     # 判断是否传递数据完整
#     if not all([name, pwd]):  # 判断是否为空
#         return {'status': 400, 'msg': '参数不完整'}
#     else:
#         # 通过用户名获取用户对象
#         user = models.User.query.filter(models.User.name == name).first()
#         # 判断用户是否存在
#         if user:
#             # 判断密码是否正确
#             if user.check_password(pwd):
#                 # 生成一个token
#                 token = generate_token({'id':user.id})
#                 return {'status':200,'msg':'登录成功','data':{'token':token}}
#         return {'status': 400, 'msg': '用户名或密码错误'}

# 登录功能
@user_bp.route('/login/', methods=['POST'])
def login():
    # 获取用户名
    # name = request.form.get('name')  # content-type: application/x-www-form-urlencoded
    name = request.get_json().get('name')  # content-type: application/json
    # 获取密码
    pwd = request.get_json().get('pwd')
    # 判断是否传递数据完整
    if not all([name, pwd]):  # 判断是否为空
        return {'status': 400, 'msg': '参数不完整'}
    else:
        # 通过用户名获取用户对象
        user = models.User.query.filter(models.User.name == name).first()
        # 判断用户是否存在
        if user:
            # 判断密码是否正确
            if user.check_password(pwd):
                # 生成一个token
                token = generate_token({'id': user.id})
                return {'status': user.role_id, 'msg': '登录成功', 'data': {'token': token}}
                # 根据role_id返回不同的状态码
                # if user.role_id == 1:
                #     return {'status': 201, 'msg': '登录成功', 'data': {'token': token},'id':user.role_id}
                # elif user.role_id == 4:
                #     return {'status': 200, 'msg': '超级管理员登录成功', 'data': {'token': token}}
                # else:
                #     # 其他role_id的情况
                #     return {'status': 200, 'msg': '登录成功', 'data': {'token': token}}
        return {'status': 400, 'msg': '用户名或密码错误'}
  
    
class Users(Resource):
    def get(self):
        # 创建RequestParser对象
        parser = reqparse.RequestParser()
        # 添加参数
        parser.add_argument('pnum',type=int,default=1,location='args')
        parser.add_argument('psize',type=int,default=2,location='args')
        parser.add_argument('name',type=str,location='args')
        # 解析参数
        args = parser.parse_args()
        # 获取里面的参数
        pnum = args.get('pnum')
        psize = args.get('psize')
        name = args.get('name')
        # 判断是否传递了name
        if name:
            # 获取用户列表
            user_list = models.User.query.filter(models.User.name.like(f'%{name}%')).paginate(page=pnum,per_page=psize)
        else:
        # 获取用户列表
            user_list = models.User.query.paginate(page=pnum,per_page=psize)
        data= {
            'total':user_list.total,
            'pnum':pnum, 
            'data':[u.to_dict() for u in user_list.items]
            }
        return {'status':200,'msg':'获取用户列表成功','data':data}


    def post(self):
        # 注册用户
        # 接收用户信息
        name = request.get_json().get('name')
        pwd = request.get_json().get('pwd')
        real_pwd = request.get_json().get('real_pwd')
        # 验证数据的合法性
        if not all([name,pwd,real_pwd]):
            return {'status':400,'msg':'数据不完整'}
        # 判断两次密码是否一致
        if pwd != real_pwd:
            return {'status':400,'msg':'两次密码不一致'}
        # 判断用户名是否合法
        if len(name) < 2:
            return {'status':400,'msg':'用户名不合法'}
        
        # 接收角色id信息
        role_id = request.get_json().get('role_id')
        
        try:
            # 判断用户名是否已经存在
            user = models.User.query.filter(models.User.name == name).first()
            if user:
                return {'status':400,'msg':'用户名已经存在'}
        except Exception as e:
            print(e)
        # 创建用户对象
        # 判断是否传递了角色id
        if role_id:
            user = models.User(name=name,password=pwd,role_id=role_id)
        else:

            user = models.User(name=name,password=pwd)
        # 添加到数据库
        db.session.add(user)
        db.session.commit()
        return {'status': 200, 'msg': '注册成功'}

user_api.add_resource(Users,'/users/')


class User(Resource):
    def get(self,id):
        user = models.User.query.get(id)
        if user:
            return {'status':200,'msg':'查询成功','data':user.to_dict()}
        else:
            return {'status':404,'msg':'用户不存在'}
    def put(self,id):
        pass
    def delete(self,id):
        try:
            user = models.User.query.get(id)
            if user:
                    db.session.delete(user)
                    db.session.commit()
            return {'status':200,'msg':'删除成功'}
        except Exception as e:
            print(e)
            return {'status':400,'msg':'删除失败'}


user_api.add_resource(User,'/user/<int:id>/')


@user_bp.route('/test/', methods=['GET'])
@login_required
def test_login_required():

    return {'status': 200, 'msg': '验证成功'}