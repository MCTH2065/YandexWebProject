import datetime

import flask_login
from flask_login import LoginManager
from flask import Flask
from data import db_session, blueprint
from data.users import User
from flask_login import login_user, logout_user, login_required
# from forms.loginform import LoginForm
# from forms.createacount import CreateAccount
# from forms.addjob import AddJob
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


@app.route('/')
def index():
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
