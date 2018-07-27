# # 命令函数
# import click
# from flask import session
#
# from app.web import web
# from git import db
#
#
# @web.cli.command()
# @click.option('--drop', is_flag=True, help='Create after drop.')
# def initdb(drop):
#     """Initialize the database."""
#     if drop:
#         db.drop_all()
#     db.create_all()
#     click.echo('Initialized database.')
#
#
# # 存储用户信息的数据库模型类
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100))  # 用户名
#     access_token = db.Column(db.String(200))  # 授权完成后获取的访问令牌
#
#
# # 管理每个请求的登录状态，如果已登录（session里有用户id值），将模型类对象保存到g对象中
# @web.before_request
# def before_request():
#     g.user = None
#     if 'user_id' in session:
#         g.user = User.query.get(session['user_id'])
#
#
# # 登入
# @web.route('/login')
# def login():
#     if session.get('user_id', None) is None:
#         ...  # 进行OAuth授权流程，具体见后面
#     flash('Already logged in.')
#     return redirect(url_for('index'))
#
#
# # 登出
# @web.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     flash('Goodbye.')
#     return redirect(url_for('index'))
