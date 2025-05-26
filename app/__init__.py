# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    from .routes import register_routes
    register_routes(app)

    # Регистрация CLI-команд
    @app.cli.command("create-db")
    def create_db_command():
        """Создает базу данных."""
        from utils.db_utils import create_database
        create_database()

    return app

