from flask_sqlalchemy import SQLAlchemy
from database_model.User import create_user_table, drop_user_table
from databas_model.Comment import create_comment_table, drop_comment_table
from sqlalchemy import inspect

db = SQLAlchemy()


#

def init_db(app):
    """
    1.配置格式：数据库类型+使用的模块://用户名:密码@服务器ip地址:端口/数据库
    2.如果设置成 True，SQLAlchemy 将会记录所有发到标准输出(stderr)的语句，可以用于调试
    3.用于设定数据库连接池的大小，默认值为10
    4.设置在连接池到达上限之后可以创建的最大连接数
    5.是否检测数据库的修改
    6.设置链接密钥
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456@localhost:5432/pruner'
    # app.config['SQLALCHEMY_ECHO'] = True
    # app.config['SQLALCHEMY_POOL_SIZE'] = 10
    # app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'xxx'

    global localApp
    localApp = app
    db.init_app(app)
    create_all(app)
    check_all(app)


def create_all(app):
    with app.app_context():
        create_user_table(db)
        create_comment_table(db)
       


def drop_all(app):
    with app.app_context():
        drop_user_table(db)
        drop_comment_table(db)




def check_all(app):
    with app.app_context():
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()

        print("Tables in the database:")
        for table_name in table_names:
            print(table_name)
