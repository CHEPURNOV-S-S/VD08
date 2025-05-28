# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Поле не должно быть пустым"),
        Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов")])
    email = StringField('Email', validators=[
        Email(message="Введите корректный email"),
        DataRequired(message="Поле не должно быть пустым")]
    )
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя уже существует.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такая почта уже используется.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(message="Введите корректный email"),
        DataRequired(message="Поле не должно быть пустым")]
    )
    password = PasswordField('Password', validators=[
        DataRequired(message="Пароль не может быть пустым")]
    )
    remember = BooleanField('Запомни меня')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super(UpdateProfileForm, self).__init__(*args, **kwargs)

    username = StringField('Имя пользователя', validators=[
        DataRequired(message="Поле не должно быть пустым"),
        Length(min=2, max=20, message="Имя должно быть от 2 до 20 символов")
    ])

    email = StringField('Email', validators=[
        DataRequired(message="Поле не должно быть пустым"),
        Email(message="Введите корректный email")
    ])

    city = StringField('Город', validators=[
        Optional(strip_whitespace=True)
    ])

    hobbies = TextAreaField('Хобби', validators=[
        Optional(strip_whitespace=True)
    ])

    age = IntegerField('Возраст', validators=[
        Optional()
    ])

    password = PasswordField('Новый пароль (опционально)', validators=[
        Optional()
    ])

    confirm_password = PasswordField('Подтвердите пароль', validators=[
        Optional(),
        EqualTo('password', message="Пароли должны совпадать")
    ])

    submit = SubmitField('Сохранить изменения')

    def validate_username(self, username):
        if self.current_user is None:
            raise ValidationError("Пользователь не определен.")

        if username.data != self.current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя пользователя занято.')

    def validate_email(self, email):
        if self.current_user is None:
            raise ValidationError("Пользователь не определен.")

        if email.data != self.current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email уже используется.')