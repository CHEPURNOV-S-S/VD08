from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename

from app import models, forms, bcrypt, db
from app.models import User
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm

from flask import current_app as app
import os


def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in app.config['ALLOWED_EXTENSIONS']

def register_routes(app):
    @app.route("/")
    def home():
        greeting = "Hello, visitor!"
        return render_template("home.html", current_user = current_user)

    @app.route("/about")
    def about():
        return render_template("about.html", team_members=team_members)

    @app.route("/blog")
    def blog():
        return render_template("blog.html", blog_posts=blog_posts)

    @app.route('/profile')
    def profile():
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        form = UpdateProfileForm(obj=current_user, current_user=current_user)
        return render_template('profile.html', user=current_user, form = form)

    @app.route("/update-profile", methods=["POST"])
    def update_profile():
        form = UpdateProfileForm(obj=current_user, current_user=current_user)
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.city = form.city.data
            current_user.hobbies = form.hobbies.data
            current_user.age = form.age.data

            if form.password.data:
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

            db.session.commit()
            flash('Профиль успешно обновлён!', 'success')
            return redirect(url_for('profile'))
        else:
            print("Ошибка подтверждения формы")
            return render_template("profile.html", form=form, current_user=current_user, show_edit_form=True)

    @app.route('/update_photo', methods=['POST'])
    def update_photo():
        if 'photo' not in request.files:
            return jsonify({'success': False, 'message': 'Файл не найден'}), 400

        file = request.files['photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Нет выбранного файла'}), 400

        if file and allowed_file(file.filename):
            # Полный путь к папке загрузок
            upload_folder = app.config['UPLOAD_FOLDER']

            # Если у пользователя уже есть своё фото (не стандартное)
            old_photo = current_user.profile_picture
            if old_photo and 'place_holder.jpg' not in old_photo:
                old_photo_path = os.path.join(upload_folder, os.path.basename(old_photo))
                if os.path.exists(old_photo_path):
                    try:
                        os.remove(old_photo_path)
                    except Exception as e:
                        print(f"Ошибка при удалении файла: {e}")
                        return jsonify({'success': False, 'message': 'Не удалось удалить старое фото'}), 500

            # Сохраняем новое фото
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, filename))
            photo_url = f"/static/uploads/{filename}"
            print(photo_url)
            # Обновляем запись в БД
            current_user.profile_picture = photo_url
            db.session.commit()

            return jsonify({'success': True, 'photo_url': photo_url})

        return jsonify({'success': False, 'message': 'Недопустимый формат файла'}), 400

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        print('Отправка формы')
        if current_user.is_authenticated:
            print('user залогинен')
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                print("успешный логин")
                return redirect(url_for('home'))
            else:
                print('Введены неверные данные', 'danger')
                form.password.errors.append("Неверный логин или пароль")
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))
