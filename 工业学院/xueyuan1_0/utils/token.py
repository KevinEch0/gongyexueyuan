'''
    1. 要加密的数据
    useid
    2. 加密算法
    pip install pyjwt
    3. 密钥
    SECREY_KEY


'''
import jwt
from functools import wraps
from flask import request
from flask import current_app
import time


# 生成token
def generate_token(data):
    '''
    data: 要加密的数据，数据类型是一个字典
    
    '''
    # 设置数据过期时间
    data.update({'exp': time.time() + current_app.config['JWT_EXPIRATION_DELTA']})
    # 数据加密
    token = jwt.encode(data,current_app.config['SECREY_KEY'], algorithm='HS256')
    return token


# 解密token
def virify_token(token):
    # 数据解密
    try:
        data = jwt.decode(token, current_app.config['SECREY_KEY'], algorithms=['HS256'])
    except Exception as e:
        return None
    return data


def login_required(view_func):
    #  登录装饰器
    @wraps(view_func)
    def verify_token_info(*args, **kwargs):
        # 获取用户传递来的token
        token = request.headers.get('token')
        # 解析token
        if virify_token(token):
            return view_func(*args, **kwargs)
        else:
            return {'status': 401 ,'msg': 'token已过期'}
        # 返回函数
    return verify_token_info
 

