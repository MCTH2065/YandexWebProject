from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class ChangeData(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    bio = StringField('О себе', validators=[DataRequired()])
    submit = SubmitField('Подтвердить изменения')
