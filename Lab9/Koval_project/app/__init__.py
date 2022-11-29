# -*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from config import config

#from .home.views import home_bp
#from .contact_form.views import contact_form_bp
#from .account.views import account_bp


db = SQLAlchemy()
login_manager = LoginManager()
# якщо є @login_required, то потім редіректить на account.login
# Фіксить помилку:
# werkzeug.routing.BuildError: Could not build url for endpoint 'login'. Did you mean 'account.login' instead?
login_manager.login_view = 'account.login'
login_manager.login_message = 'Please, sign in to access to the account'
login_manager.login_message_category = 'info'
migrate = Migrate()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager.init_app(app)

    with app.app_context():
        #app.register_blueprint(home_bp, url_prefix="/home")
        #app.register_blueprint(contact_form_bp, url_prefix="/contact_form")
        #app.register_blueprint(account_bp, url_prefix="/account")

        from app.home import home_bp
        from app.contact_form import contact_form_bp
        from app.account import account_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(contact_form_bp)
        app.register_blueprint(account_bp)

    return app
