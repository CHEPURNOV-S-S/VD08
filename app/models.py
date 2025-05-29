# app/models.py
from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    __table_args__ = (
        UniqueConstraint('username', name='uq_user_username'),
        UniqueConstraint('email', name='uq_user_email'),
    )

    password = db.Column(db.String(60), nullable=False)

    # Дополнительные поля для профиля
    city = db.Column(db.String(100), nullable=True)  # Город
    hobbies = db.Column(db.Text, nullable=True)  # Хобби (может быть много строк)
    age = db.Column(db.Integer, nullable=True)  # Возраст
    profile_picture = db.Column(db.String(255), nullable=True)  # Путь к фото профиля

    def __repr__(self):
        return f'User: {self.name}, email: {self.email}'
