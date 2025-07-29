import os


class Config:
    # 设置参数
    MYSQL_DIALECT = 'mysql'
    MYSQL_DRIVER = 'pymysql'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_DB = 'gongyexueyuan'
    MYSQL_CHARSET = 'utf8mb4'

    # 数据库连接字符串
    SQLALCHEMY_DATABASE_URI = f'{MYSQL_DIALECT}+{MYSQL_DRIVER}://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset={MYSQL_CHARSET}'
    # 数据盐
    SECREY_KEY = os.urandom(16)
    # 设置JSON数据不适用ASCII编码
    JSON_AS_ASCII = False
    RESTFUL_JSON = {'ensure_ascii': False}

    # 设置token过期的时间
    JWT_EXPIRATION_DELTA = 60 * 60 * 24 * 7


class DevelopmentConfig(Config):
  # 开发环境
  # DEBUG模式
  DEBUG = True

class ProductionConfig(Config):
  # 生产环境
  DEBUG = False

class TestingConfig(Config):
  # 测试环境
  pass

config_map = {
  'develop': DevelopmentConfig, # 开发环境
  'product': ProductionConfig, # 生产环境
  'test': TestingConfig # 测试环境
}
