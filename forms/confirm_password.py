from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired


class ConfirmPassword(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    check_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Подтвердить данные')
