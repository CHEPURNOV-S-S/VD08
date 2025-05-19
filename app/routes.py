# app/routes.py

from flask import render_template
from app import create_app

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/blog')
    def blog():
        return render_template('blog.html')

    @app.route('/contacts')
    def contacts():
        return render_template('contacts.html')