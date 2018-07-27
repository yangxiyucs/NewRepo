# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# from app.web import web
#
# db = SQLAlchemy()
#
#
# def register_web_blueprint(app):
#     from app.web import web
#     app.register_blueprint(web)
#
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object('app.setting')
#
#     register_web_blueprint(app)
#     db.init_app(app)
