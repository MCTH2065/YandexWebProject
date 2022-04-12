import datetime

import flask_login
from flask_login import LoginManager
from flask import Flask
from data import db_session, blueprint
from data.users import User
from flask_login import login_user, logout_user, login_required
# from forms.loginform import LoginForm
# from forms.addjob import AddJob
from flask import request
from forms.user_change import ChangeData
from forms.createaccount import CreateAccount
from forms.loginform import LoginForm
import random
from data.jobs import Jobs
from flask import render_template
from flask import redirect, make_response
from flask import jsonify
from flask import session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    logout_user()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            res = make_response(redirect("/"))
            data = '-'.join([user.name, user.surname, str(user.age), user.email, str(user.rating),
                             str(user.experience), str(user.money), str(user.mood), user.bio,
                             str(user.id)])
            session["user"] = data
            return res
        res = make_response(render_template('login.html',
                                            message="Неправильный логин или пароль",
                                            form=form,
                                            data="Только авторизованные пользователи могут пользоваться сервисом Work At Home"))
        session.pop("user", None)
        return res
    res = make_response(render_template('login.html', form=form, data="Только авторизованные пользователи"
                                                                      " могут пользоваться сервисом"
                                                                      " Work At Home"))
    session.pop("user", None)
    return res


@app.route('/create', methods=['GET', 'POST'])
def create():
    logout_user()
    form = CreateAccount()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data == form.check_password.data:
            if db_sess.query(User).filter(User.email == form.email.data).all == []:
                user = User()
                user.surname = form.surname.data
                user.name = form.name.data
                user.age = form.age.data
                user.email = form.email.data
                user.hashed_password = form.password.data
                user.experience = form.experience.data
                user.bio = form.bio.data
                db_sess.add(user)
                db_sess.commit()
                res = make_response(redirect("/login"))
                session.pop("user", None)
                return res
            else:
                res = make_response(render_template('createaccount.html',
                                                    message="Почта занята",
                                                    form=form))
                return res
        res = make_response(render_template('createaccount.html',
                                            message="Пароли не совпадают",
                                            form=form))
        session.pop("user", None)
        return res
    res = make_response(render_template('createaccount.html', form=form))
    session.pop("user", None)
    return res


@app.route('/')
def index():
    us = session.get("user", 0)
    db_sess = db_session.create_session()
    if us == 0:
        return redirect("/login")
    else:
        user = db_sess.query(User).filter(User.email == us.split('-')[3]).first()
        return render_template('main.html', data=' '.join([user.name, user.surname]))


@login_required
@app.route('/jobs')
def jobs():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    db_s = db_session.create_session()
    j = db_s.query(Jobs).all()
    data = []
    for elem in j:
        ch = random.randint(1, 10)
        if ch / 10 <= elem.chance_of_a_job:
            stats = random.choice(elem.field_rating_mood_salary.split(', ')).split('-')
            d = [elem.name, elem.about, elem.boss,
                 random.choice(elem.lower_rank_bosses.split(', ')),
                 stats[0], stats[1], stats[2], stats[3]
                 ]
            data.append(d)

    return render_template('jobs.html', data=data)


@app.route('/work')
def work():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    return render_template('workwork.html')


@app.route('/company')
def company_info():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    return render_template('company.html')


@app.route('/user')
def user_data():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    return render_template('user_data.html', data=us.split('-'))


@app.route('/user_change', methods=['GET', 'POST'])
def user_data_change():
    form = ChangeData()
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    if form.is_submitted():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == us.split('-')[9]).all != []:
            if us.split('-')[3] == form.email.data or \
                    db_sess.query(User).filter(User.email == form.email.data).all() == []:
                user = db_sess.query(User).filter(User.id == us.split('-')[9]).one()
                user.name = form.name.data
                user.surname = form.surname.data
                user.age = form.age.data
                user.email = form.email.data
                user.bio = form.bio.data
                db_sess.commit()
                user = db_sess.query(User).filter(User.id == us.split('-')[9]).one()
                data = '-'.join([user.name, user.surname, str(user.age), user.email, str(user.rating),
                                 str(user.experience), str(user.money), str(user.mood), str(user.bio),
                                 str(user.id)])
                session["user"] = data
                return redirect('/user')

        return render_template('user_data_change.html', data=us.split('-'), form=form,
                               message='Почта уже занята')
    return render_template('user_data_change.html', data=us.split('-'), form=form)


def main():
    db_session.global_init("db/top_secret.db")
    # s = db_session.create_session()
    # j = Jobs()
    # j.name = 'dggd'
    # j.about = 'gf'
    # j.boss = 'df'
    # j.lower_rank_bosses = 'gf'
    # j.field_rating_mood_salary = 'IT-79-63-35'
    # s.add(j)
    # s.commit()
    app.run()


if __name__ == '__main__':
    main()
