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
from forms.createaccount import CreateAccount
from forms.loginform import LoginForm
import random
from data.jobs import Jobs
from flask import render_template
from flask import redirect, make_response
from flask import jsonify

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
            login_user(user, remember=form.remember_me.data)
            res = make_response(redirect("/"))
            data = '-'.join([user.name, user.surname, str(user.age), user.email, str(user.rating),
                             str(user.experience), str(user.money), str(user.mood), user.bio])
            res.set_cookie("user", data, max_age=60 * 60 * 24 * 365 * 2)
            return res
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateAccount()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.password.data == form.check_password.data:
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
            return redirect("/login")
        return render_template('createaccount.html',
                               message="Пароли не совпадают",
                               form=form)
    return render_template('createaccount.html', form=form)

@app.route('/')
def index():
    u = request.cookies.get("user", 0)
    print(u)
    if u == 0:
       return redirect("/login")
    else:
        print(flask_login.current_user)
        return render_template('main.html')


@app.route('/jobs')
def jobs():
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
    return render_template('workwork.html')


@app.route('/company')
def company_info():
    return render_template('company.html')


@app.route('/user')
def user_data():
    return render_template('user_data.html')


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
