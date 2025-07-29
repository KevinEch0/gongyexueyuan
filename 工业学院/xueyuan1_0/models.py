from xueyuan1_0 import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class BaseModel(object): 
  create_time = db.Column(db.DateTime, default=datetime.now)
  update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



class User(db.Model,BaseModel):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True , nullable=False)
    pwd = db.Column(db.String(256))

    # 建立用户和角色的关系：多对1关系
    role_id = db.Column(db.Integer, db.ForeignKey('t_role.id'))


    @property
    def password(self):
        return self.pwd
    
    @password.setter
    def password(self, pwd):
        # 数据密码数据加密
        self.pwd = generate_password_hash(pwd)   # 数据加密

    def check_password(self, pwd):
        # 检查密码是否匹配
        return check_password_hash(self.pwd, pwd)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role_name': self.role.name if self.role else '',
            'role_id':self.role.id if self.role else '',
        }
    
trm = db.Table(
    't_roles_menus',
    db.Column('role_id',db.Integer,db.ForeignKey('t_role.id')),
    db.Column('menu_id',db.Integer,db.ForeignKey('t_menu.id'))
)
    
class Menu(db.Model):
    __tablename__ = 't_menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True,nullable=False)
    level = db.Column(db.Integer, default=1)
    path = db.Column(db.String(32))

    pid = db.Column(db.Integer, db.ForeignKey('t_menu.id'))
    children = db.relationship('Menu')
    roles = db.relationship('Role', secondary=trm,backref='menus')

    def to_dict_tree(self):
        return {
        'id': self.id,
        'name': self.name,
        'path': self.path,
        'level': self.level,
        'pid': self.pid,
        'children': [child.to_dict_tree() for child in self.children]
        }
    def to_dict_list(self):
        return {
        'id': self.id,
        'name': self.name,
        'path': self.path,
        'level': self.level,
        'pid': self.pid,
        }

class Role(db.Model):
    __tablename__ = 't_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    desc = db.Column(db.String(256))

    # 建立角色与用户的关系：1对多
    users = db.relationship('User',backref='role')
    # menus = db.relationship('Menu', secondary=trm)
    def to_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'desc': self.desc,
        # 'menus': [menu.to_dict_tree() for menu in self.menus if menu.level == 1]
        'menus': self.get_menu_dict()
        }
    
    def get_menu_dict(self):
        # 创建一列表存储所有的菜单
        menu_list = []
        menus = sorted(self.menus,key=lambda temp:temp.id)
        
        # 查询所有的一级菜单
        for m in menus:
            if m.level == 1:
                first_dict = m.to_dict_list()
                first_dict['children'] = []
                
                # 查询所有的二级菜单
                for m2 in menus:
                    if m2.level == 2 and m2.pid == m.id:
                        second_dict = m2.to_dict_list()
                        second_dict['children'] = []
                        
                        # 查询所有的三级菜单
                        for m3 in menus:
                            if m3.level == 3 and m3.pid == m2.id:
                                third_dict = m3.to_dict_list()
                                second_dict['children'].append(third_dict)
                        
                        first_dict['children'].append(second_dict)
                
                menu_list.append(first_dict)
        
        return menu_list