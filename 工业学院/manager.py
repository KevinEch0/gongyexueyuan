from flask_migrate import Migrate

from xueyuan1_0 import create_app,db

from flask_cors import CORS

app = create_app('develop')

CORS(app, supports_credentials=True) # 解决跨域问题


# 创建同步数据库的对象
Migrate(app, db)


'''
flask db init 初始化数据库同步文件
flask db migrate 生成数据库表文件
flask db upgrade 同步数据库

'''



if __name__ == '__main__':
    app.run()