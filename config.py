# config_template.py

import os
#this is template of config file.

class Config:
    DEBUG = True

    UPLOAD_FOLDER = 'app/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    API_NINJAS_KEY = os.environ.get('API_NINJAS_KEY')

    REQUIRED_VARS = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'API_NINJAS_KEY']