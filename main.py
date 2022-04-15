import datetime

import flask_login
from flask_login import LoginManager
from flask import Flask
from data import db_session, blueprint
from data.serverdata import ServerData
from data.users import User
from flask_login import login_user, logout_user, login_required
# from forms.loginform import LoginForm
# from forms.addjob import AddJob
from flask import request
from forms.confirm_password import ConfirmPassword
from forms.user_change import ChangeData
from forms.createaccount import CreateAccount
from forms.loginform import LoginForm
from forms.forgotpassword import ForgotPassword
from forms.changepassword import ChangePassword
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
            if user.comp:
                company = db_sess.query(Jobs).filter(Jobs.id == int(user.comp)).one().name
            else:
                company = ''
            data = 'UgandaWillNeverBeChosenAsABioOfSomeoneRight?'.join(
                [user.name, user.surname, str(user.age), user.email, str(user.rating),
                 str(user.experience), str(user.money), str(user.mood), user.bio,
                 str(user.id), str(user.pfp), company])
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
            if db_sess.query(User).filter(User.email == form.email.data).all() == []:
                user = User()
                user.surname = form.surname.data
                user.name = form.name.data
                user.age = form.age.data
                user.email = form.email.data
                user.hashed_password = form.password.data
                user.experience = form.experience.data
                user.bio = form.bio.data
                user.codeword = form.codeword.data
                user.pfp = f'static/img/{str(random.randint(1, 6))}.png'
                db_sess.add(user)
                db_sess.commit()
                session.pop("user", None)
                return redirect('/login')
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
        user = db_sess.query(User).filter(
            User.email == us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[3]).first()
        return render_template('main.html', data=' '.join([user.name, user.surname]))


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    message = session.get("message_for_job", "")
    db_s = db_session.create_session()
    current = db_s.query(ServerData).one()
    dif = (datetime.datetime.now() - current.modified_date).seconds
    if dif >= 5:
        j = db_s.query(Jobs).all()
        data = []
        for_db = []
        for elem in j:
            ch = random.randint(1, 10)
            if ch / 10 <= elem.chance_of_a_job:
                stats = random.choice(elem.field_rating_mood_salary.split(', ')).split('-')
                b = random.choice(elem.lower_rank_bosses.split(', '))
                d = [elem.name, elem.about, elem.boss,
                     b, stats[0], stats[1], stats[2], stats[3], elem.is_experience_required
                     ]
                for_db.append(
                    f'{str(elem.id)}-{stats[0]}-{stats[1]}-{stats[2]}-{stats[3]}-{b}')
                data.append(d)
        current.current_jobs = (';'.join(for_db))
        current.modified_date = datetime.datetime.now()
        db_s.commit()
        session.pop("message_for_job", None)
        return render_template('jobs.html', data=data, message=message)
    else:
        data = []
        if current.current_jobs:
            for elem in current.current_jobs.split(';'):
                j = db_s.query(Jobs).filter(Jobs.id == int(elem.split('-')[0])).one()
                stats = elem.split('-')[1:6]
                d = [j.name, j.about, j.boss, (stats[4]),
                     stats[0], stats[1], stats[2], stats[3], j.is_experience_required
                     ]
                data.append(d)
        session.pop("message_for_job", None)
        return render_template('jobs.html', data=data, message=message)


@app.route('/get_job', methods=['GET', 'POST'])
def test():
    db_s = db_session.create_session()
    current = db_s.query(ServerData).one()
    dif = (datetime.datetime.now() - current.modified_date).seconds
    d = request.form.get('data')
    d = d.split('"')
    company_name = d[-2]
    c = db_s.query(Jobs).filter(Jobs.name == company_name).one()
    user = session.get("user").split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    if user[11]:
        session["message_for_job"] = 'already'
    else:
        if dif <= 5:
            r = user[4]
            exp = user[5]
            mood = user[7]
        else:
            r = -1000000
            exp = False
            mood = -1000000
            session["message_for_job"] = '0'
        stats = c.field_rating_mood_salary.split('-')
        if int(r) >= 0:
            if int(r) >= int(stats[1]):
                if int(mood) >= int(stats[2]):
                    if (str(c.is_experience_required) == 'True' and str(exp) == 'True') \
                            or (str(c.is_experience_required) == 'False'):
                        field_head = current.current_jobs.split(';')
                        head = None
                        field = None
                        for elem in field_head:
                            if str(elem.split('-')[0]) == str(c.id):
                                head = elem.split('-')[5]
                                field = elem.split('-')[1]
                        userid = int(user[9])
                        u = db_s.query(User).filter(User.id == userid).one()
                        company = db_s.query(Jobs).filter(Jobs.id == int(c.id)).one().makes_happier
                        if u.mood + company <= 100:
                            u.mood += company
                        else:
                            u.mood = 100
                        u.comp = c.id
                        u.head = head
                        u.field = field
                        db_s.commit()
                        u = db_s.query(User).filter(User.id == userid).one()
                        company = db_s.query(Jobs).filter(Jobs.id == int(u.comp)).one()
                        company_n = company.name
                        data = 'UgandaWillNeverBeChosenAsABioOfSomeoneRight?'.join(
                            [u.name, u.surname, str(u.age), u.email, str(u.rating),
                             str(u.experience), str(u.money), str(u.mood), u.bio,
                             str(u.id), str(u.pfp), company_n])
                        session["user"] = data
                        session["message_for_job"] = '1'
                    else:
                        session["message_for_job"] = 'отсутсвие опыта'
                else:
                    session["message_for_job"] = 'низкий коэфицент трудоспособности'
            else:
                session["message_for_job"] = 'низкий рейтинг'

    return redirect('/jobs')


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
    db_s = db_session.create_session()
    user = us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    company_name = user[11]
    if company_name:
        company = db_s.query(Jobs).filter(Jobs.name == company_name).one()
        j = []
        for elem in company.field_rating_mood_salary.split(', '):
            j.append(elem.split('-')[0])
        j = ', '.join(j)
        more_user = db_s.query(User).filter(User.id == int(user[9])).one()

        company_data = [company.name, company.boss, company.lower_rank_bosses, j, company.more_about,
                        more_user.head, more_user.field]
        return render_template('company.html', data=company_data)
    else:

        return render_template('company.html')


@app.route('/resign', methods=['GET', 'POST'])
def resign():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    form = ConfirmPassword()
    if form.is_submitted():
        if form.password.data == form.check_password.data:
            s = db_session.create_session()
            userid = us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[9]

            com = s.query(Jobs).filter(
                Jobs.name == (us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[11])).one().makes_sadder
            usdata = s.query(User).filter(User.id == userid).one()
            if usdata.mood - int(com) >= 0:
                usdata.mood -= int(com)
            else:
                usdata.mood = 0
            usdata.comp = None
            usdata.head = None
            usdata.field = None
            s.commit()
            u = s.query(User).filter(User.id == userid).one()
            data = 'UgandaWillNeverBeChosenAsABioOfSomeoneRight?'.join(
                [u.name, u.surname, str(u.age), u.email, str(u.rating),
                 str(u.experience), str(u.money), str(u.mood), u.bio,
                 str(u.id), str(u.pfp), ''])
            session["user"] = data
            return redirect("/")
        return render_template('confirm_password.html', form=form,
                               message='Пароли не совпадают!')
    return render_template('confirm_password.html', form=form)


@app.route('/user')
def user_data():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    return render_template('user_data.html', data=us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?'))


@app.route('/user_change', methods=['GET', 'POST'])
def user_data_change():
    form = ChangeData()
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    if form.is_submitted():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.id == us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[9]).all != []:
            if us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[3] == form.email.data or \
                    db_sess.query(User).filter(User.email == form.email.data).all() == []:
                user = db_sess.query(User).filter(
                    User.id == us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[9]).one()
                user.name = form.name.data
                user.surname = form.surname.data
                user.age = form.age.data
                user.email = form.email.data
                user.bio = form.bio.data
                db_sess.commit()
                user = db_sess.query(User).filter(
                    User.id == us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[9]).one()
                if user.comp:
                    company = db_sess.query(Jobs).filter(Jobs.id == int(user.comp)).one().name
                else:
                    company = ''
                data = 'UgandaWillNeverBeChosenAsABioOfSomeoneRight?'.join(
                    [user.name, user.surname, str(user.age), user.email, str(user.rating),
                     str(user.experience), str(user.money), str(user.mood), user.bio,
                     str(user.id), str(user.pfp), company])
                session["user"] = data
                return redirect('/user')

        return render_template('user_data_change.html', data=us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?'),
                               form=form,
                               message='Почта уже занята')
    return render_template('user_data_change.html', data=us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?'),
                           form=form)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotPassword()
    if form.is_submitted():
        s = db_session.create_session()
        u = s.query(User).filter(User.email == form.email.data,
                                 User.name == form.name.data,
                                 User.surname == form.surname.data,
                                 User.codeword == form.codeword.data).all()
        if len(u) == 1:
            session["change_password"] = u[0].id
            return redirect('/change_password')
        return render_template('forgotpassword.html', form=form,
                               message='Неверные данные!')
    return render_template('forgotpassword.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    u = session.get("change_password", 0)
    if u == 0:
        return redirect("/login")
    form = ChangePassword()
    if form.is_submitted():
        if form.password.data == form.check_password.data:
            s = db_session.create_session()
            user = s.query(User).filter(User.id == u).one()
            if form.password.data == user.hashed_password:
                return render_template('changepassword.html', form=form,
                                       message='Нельзя использовать'
                                               ' предыдущий пароль!')
            user.hashed_password = str(form.password.data)
            s.commit()
            return redirect("/")
        return render_template('changepassword.html', form=form,
                               message='Пароли не совпадают!')
    return render_template('changepassword.html', form=form)


def main():
    db_session.global_init("db/top_secret.db")
    # s = db_session.create_session()
    # s.commit()

    app.run()


if __name__ == '__main__':
    main()
