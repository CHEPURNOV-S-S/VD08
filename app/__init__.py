# app/__init__.py

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print(f"Config.ALLOWED_EXTENSIONS: {Config.ALLOWED_EXTENSIONS}")
    print("Config['ALLOWED_EXTENSIONS']:", app.config['ALLOWED_EXTENSIONS'])
    print("Config['UPLOAD_FOLDER']:", app.config['UPLOAD_FOLDER'])

    from .routes import register_routes
    register_routes(app)

    return app