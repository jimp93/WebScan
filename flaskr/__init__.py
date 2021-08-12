import os

from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy


def create_app(dev):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # g.mode = mode

    # if mode == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\james\\PycharmProjects\\WebScan\\flaskr\\sqlite.db'
    app.config['SECRET_KEY'] = 'dev'

    # else:
    #     app.debug =  False
    #     app.config['SECRET_KEY'] ='/KQS^K8Ns^.qv?E'
    #     app.config['SQLALCHEMY_DATABASE_URI'] = ''

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # create sqalchemy object called db in dbp
    # prepare app settings that db will need to learn about to carry out procedures. N
    # Needs to know which app it is serving
    # before executing the procedure, push the settings (no auto app context if not view function)
    # can use app as parameter for some procedures
    # db and app are separate objects, passing app into db just gives necessary db config info
    from flaskr.dbp import db
    db.init_app(app)
    # calls function to make cli create tables command, while also creating an app context for db to bind to.
    # (see fn code)
    from flaskr.dbp import init_app_inst
    init_app_inst(app)

    from flaskr import auth
    app.register_blueprint(auth.bp)

    from flaskr import index
    app.register_blueprint(index.bp)
    # index
    app.add_url_rule('/', endpoint='index')

    return app
