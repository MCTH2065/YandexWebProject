from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangePassword(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    check_password = PasswordField('Подтвердите пароль', validators=[DataRequired()])
    submit = SubmitField('Изменить пароль')