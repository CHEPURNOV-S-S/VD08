# app/__init__.py
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate



from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    for var in app.config['REQUIRED_VARS']:
        if not app.config.get(var):
            raise ValueError(f"Не задана переменная окружения: {var}")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate.init_app(app, db)

    from .routes import register_routes
    register_routes(app)

    # Регистрация CLI-команд
    @app.cli.command("create-db")
    def create_db_command():
        """Создает базу данных."""
        from utils.db_utils import create_database
        create_database()

    # Регистрация CLI-команд
    @app.cli.command("secret-gen")
    def generate_secret_command():
        """Создает базу данных."""
        from utils.secret_gen import generate_secret
        generate_secret()

    return app

