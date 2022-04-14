from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class CreateAccount(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    check_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    codeword = StringField('Кодовое слово', validators=[DataRequired()])
    bio = StringField('Напишите что-нибудь о себе', validators=[DataRequired()])
    experience = BooleanField('Наличие опыта работы')
    submit = SubmitField('Создать аккаунт')
