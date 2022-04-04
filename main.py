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
# from data.jobs import Jobs
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




def main():
    db_session.global_init("db/top_secret.db")
    db_sess = db_session.create_session()
    us = User()
    us.surname = 'Chalov'
    us.name = 'Matt'
    us.age = 16
    us.email = 'cor_n@mail.ru'
    us.hashed_password = '123456'
    us.experience = True
    us.bio = 'Yandex Lyceum student'
    db_sess.add(us)
    db_sess.commit()
    # app.register_blueprint(blueprint.blueprint)
    app.run()






if __name__ == '__main__':
    main()
