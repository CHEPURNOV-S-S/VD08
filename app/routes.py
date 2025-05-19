from flask import Flask, render_template

app = Flask(__name__)

# Данные для шаблона about.html
team_members = [
    {"name": "Simon", "role": "Developer"},
    {"name": "Semyon", "role": "Designer"},
    {"name": "Simeon", "role": "Manager"}
]

# Данные для шаблона blog.html
blog_posts = [
    {"title": "Introduction to Python"},
    {"title": "Flask Basics"},
    {"title": "Web Development with Jinja"}
]


def register_routes(app):
    @app.route("/")
    def home():
        greeting = "Hello, visitor!"
        return render_template("home.html", greeting=greeting)

    @app.route("/about")
    def about():
        return render_template("about.html", team_members=team_members)

    @app.route("/blog")
    def blog():
        return render_template("blog.html", blog_posts=blog_posts)

