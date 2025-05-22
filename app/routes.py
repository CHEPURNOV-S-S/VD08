from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import current_app as app
import os
from werkzeug.utils import secure_filename

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

# Инициализация данных пользователя
user_data = {
    'name': 'Анна',
    'city': 'Москва',
    'hobby': 'Чтение книг',
    'age': 25,
    'photo': '/static/place_holder.jpg'  # Путь к дефолтной фотографии
}

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in app.config['ALLOWED_EXTENSIONS']

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

    @app.route('/profile', methods=['GET'])
    def profile():
        """Отображение профиля пользователя"""
        return render_template('profile.html',
                               user_name=user_data['name'],
                               user_city=user_data['city'],
                               user_hobby=user_data['hobby'],
                               user_age=user_data['age'],
                               user_photo=user_data['photo'])

    @app.route('/edit_profile', methods=['GET', 'POST'])
    def edit_profile():
        """Редактирование профиля пользователя"""
        if request.method == 'POST':
            # Обновляем данные пользователя
            user_data['name'] = request.form.get('name')
            user_data['city'] = request.form.get('city')
            user_data['hobby'] = request.form.get('hobby')
            user_data['age'] = request.form.get('age')
            flash('Данные успешно обновлены!', 'success')
            return redirect(url_for('profile'))
        return render_template('profile.html',
                               user_name=user_data['name'],
                               user_city=user_data['city'],
                               user_hobby=user_data['hobby'],
                               user_age=user_data['age'],
                               user_photo=user_data['photo'])

    @app.route('/update_photo', methods=['POST'])
    def update_photo():
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'Файл не найден'}), 400

        file = request.files['photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Нет выбранного файла'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_url = f"/static/uploads/{filename}"
            return jsonify({'success': True, 'photo_url': photo_url})

        return jsonify({'success': False, 'message': 'Недопустимый формат файла'}), 400

