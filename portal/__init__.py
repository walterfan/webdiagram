import logging
import os
import sys
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from .auth.models import User
from .auth.models import Category

def create_logger(filename, log2console=True, logLevel=logging.INFO, logFolder='./logs'):
    # add log
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    formats = '%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)s - %(message)s'
    formatter = logging.Formatter(formats)

    logfile = os.path.join(logFolder, filename + '.log')
    directory = os.path.dirname(logfile)
    if not os.path.exists(directory):
        os.makedirs(directory)

    handler = logging.FileHandler(logfile)
    handler.setLevel(logLevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log2console:
        handler2 = logging.StreamHandler(sys.stdout)
        handler2.setFormatter(logging.Formatter(formats))
        handler2.setLevel(logLevel)
        logger.addHandler(handler2)

    return logger

def register_module(app):
    from .diagram import diagram_module as diagram_blueprint
    from .auth import auth_module as auth_blueprint
    from .main import main_module as main_blueprint


    app.register_blueprint(diagram_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        user = User.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(user=user, categories=categories)

def create_app(env_name="default"):
    app = Flask("portal")
    app.config.from_object(config[env_name])
    #app.config["SECRET_KEY"] = "secret"
    config[env_name].init_app(app)

    config_name = os.getenv('FLASK_CONFIG') or 'default'

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)


    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    register_module(app)
    register_template_context(app)

    return app

logger = create_logger("webdiagram")




