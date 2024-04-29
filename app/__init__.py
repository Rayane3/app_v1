from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Adjust the login view

    from .routes.main_routes import main
    from .routes.auth_routes import auth
    from .routes.booking_routes import booking

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(booking)

    return app

