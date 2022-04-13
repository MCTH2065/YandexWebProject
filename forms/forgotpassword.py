from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, StringField
from wtforms.validators import DataRequired


class ForgotPassword(FlaskForm):
    email = EmailField("Почта", validators=[DataRequired()])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    codeword = StringField("Кодовое слово", validators=[DataRequired()])
    submit = SubmitField('Подтвердить данные')
