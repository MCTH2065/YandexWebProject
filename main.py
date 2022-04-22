import datetime

import os
from flask_login import LoginManager
from flask import Flask
from data import db_session
from data.serverdata import ServerData
from data.users import User
from flask_login import login_user, logout_user
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


def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def update_job():
    us = session.get("user", 0)
    db_s = db_session.create_session()
    us_data = us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    us_id = us_data[9]
    u = db_s.query(User).filter(User.id == str(us_id)).one()
    if u.work_is_done == False:
        if not u.work:
            field = u.field
            if field == 'IT':
                funcs = [['для вывода в консоль', 'print, print()'], ['для перевода данных в строку', 'str, str()'],
                         ['для перевода данных в целое число', 'int, int()'],
                         ['для перевода данных в число с плавающей запятой', 'float, float()'],
                         ['для присваивания значений', '='], ['для перевода данных в список',
                                                              'list, list(), []'],
                         ['для перевода данных в множество', 'set, set()'],
                         ['для перевода данных в словарь', 'dict, dict(), {}'],
                         ['для перевода данных в кортеж', 'tuple, tuple(), ()']]
                ran_first = random.randint(1, 10000)
                first = f'Чему будет равно число {str(ran_first)} в двоичной системе счисления?'
                ans_first = str(format(ran_first, 'b'))

                ran_second = random.randint(1, 10000)
                second = f'Чему будет равно число {str(ran_second)} в четверичной системе счисления?'
                ans_second = ''.join(str(number_to_base(ran_second, 4))[1:-1].split(', '))

                ran_third = random.randint(1, 10000)
                third = f'Чему будет равно число {str(ran_third)} в восьмеричной системе счисления?'
                ans_third = ''.join(str(number_to_base(ran_third, 8))[1:-1].split(', '))

                ran_fourth = random.choice(funcs)
                fourth = f'Что служит в Python {ran_fourth[0]}?'
                ans_fourth = ran_fourth[1].split(', ')

                print(ans_first, ans_second, ans_third, ans_fourth)

                f = 'question-answer'.join([first, ans_first])
                s = 'question-answer'.join([second, ans_second])
                t = 'question-answer'.join([third, ans_third])
                ft = 'question-answer'.join([fourth, str(ans_fourth)])
                user_work = 'between-tasks'.join([f, s, t, ft])
                u.work = user_work
                db_s.commit()
                session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]
            elif field == 'Economics':
                ran_first = random.randint(20, 80)
                ran_days_first = random.randint(18, 22)
                ran_hours_first = random.randint(7, 9)
                first = f'Сколько денег в конце месяца, в котором {ran_days_first} рабочих дней,' \
                        f' получит работник, который работает {ran_hours_first} часов в день с зарплатой {ran_first}' \
                        f' д/ч'
                ans_first = ran_first * ran_hours_first * ran_days_first
                print(ans_first)

                ran_second = random.randint(20, 80)
                ran_days_second = random.randint(18, 22)
                ran_hours_second = random.randint(7, 9)
                second = f'Сколько денег в конце месяца, в котором {ran_days_second} рабочих дней,' \
                         f' получит работник, который работает {ran_hours_second}' \
                         f' часов в день с зарплатой {ran_second} д/ч'
                ans_second = ran_first * ran_hours_second * ran_days_second
                print(ans_second)

                ran_third_money = random.choice([5000, 8000, 10000, 6000, 9000, 14000])
                ran_third_f = random.choice([2, 4, 8])
                ran_third_s = random.choice([2, 4, 8])
                third = f'Вам из {ran_third_f} офисов пришло по {ran_third_money} долларов.' \
                        f' По сколько долларов получит каждый из {ran_third_s} других офисов?'
                ans_third = (ran_third_money * ran_third_f) // ran_third_s
                print(ans_third)

                ran_fourth_money = random.choice([50000, 70000, 80000, 90000, 100000, 110000, 120000, 130000])
                ran_fourth_losses = random.choice([60, 70, 80])
                fourth = f'Предприятие в среднем зарабатывает {ran_fourth_money} долларов.' \
                         f' Какова будет чистая прибыль в год, если расходы равны {ran_fourth_losses} процентов?'
                ans_fourth = int((ran_fourth_money * 12) * ((100 - ran_fourth_losses) / 100))
                print(ans_fourth)

                f = 'question-answer'.join([first, str(ans_first)])
                s = 'question-answer'.join([second, str(ans_second)])
                t = 'question-answer'.join([third, str(ans_third)])
                ft = 'question-answer'.join([fourth, str(ans_fourth)])

                user_work = 'between-tasks'.join([f, s, t, ft])
                u.work = user_work
                db_s.commit()
                session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]

            elif field == 'Engineering':
                ran_first_value = random.randint(500, 2500)
                ran_first_volume = random.randint(1, 25)
                first = f'Чему равна масса тела плотности {ran_first_value} кг/куб. метр и ' \
                        f'объема {ran_first_volume} куб. метров?'
                ans_first = ran_first_value * ran_first_volume

                second_voltage = 220
                random_second_current = random.choice([5, 10, 11, 22, 44])
                second = f'Чему равно сопротивление проводника в сети, напряжение в которой равно {second_voltage}' \
                         f' вольт, а сила тока равна {random_second_current} ампер?'
                ans_second = second_voltage // random_second_current

                third_random_length = random.randint(5, 30)
                third_random_height = random.randint(5, 15)
                third_random_radius = random.randint(2, 10)
                third = f'Чему равна площадь цилиндра (число пи принять за 3), высота боковой стороны которого равна' \
                        f' {third_random_height} метров, её длина равна {third_random_length} метров,' \
                        f' а радиус основания равен {third_random_radius} метров?'
                ans_third = (third_random_length * third_random_height) + 2 * (3 * (third_random_radius ** 2))

                fourth_random_av_speed = random.randint(50, 150)
                fourth_random_hours = random.randint(2, 15)
                fourth = f'Какой путь пройдёт автомобиль, двигаясь со средней скоростью {fourth_random_av_speed}' \
                         f' километров в час {fourth_random_hours} часов?'
                ans_fourth = fourth_random_av_speed * fourth_random_hours

                f = 'question-answer'.join([first, str(ans_first)])
                s = 'question-answer'.join([second, str(ans_second)])
                t = 'question-answer'.join([third, str(ans_third)])
                ft = 'question-answer'.join([fourth, str(ans_fourth)])

                user_work = 'between-tasks'.join([f, s, t, ft])
                u.work = user_work
                db_s.commit()
                session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]

        else:
            tasks = u.work.split('between-tasks')
            f = tasks[0]
            s = tasks[1]
            t = tasks[2]
            ft = tasks[3]
            first, ans_first = f.split('question-answer')[0], f.split('question-answer')[1]
            second, ans_second = s.split('question-answer')[0], s.split('question-answer')[1]
            third, ans_third = t.split('question-answer')[0], t.split('question-answer')[1]
            fourth, ans_fourth = ft.split('question-answer')[0], ft.split('question-answer')[1]
            session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]
            user = session.get("user").split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
            id = int(user[9])
            real_user = db_s.query(User).filter(User.id == id).one()
            if real_user.mood + 2 >= 100:
                real_user.mood = 100
            else:
                real_user.mood += 2
            db_s.commit()


def register_time():
    db_s = db_session.create_session()
    user = session.get("user").split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    id = int(user[9])
    real_user = db_s.query(User).filter(User.id == id).one()
    if real_user.work_time:
        last = real_user.work_time
        now = datetime.datetime.today()
        if now - last >= datetime.timedelta(seconds=86400):
            real_user.work_time = now
            real_user.work = None
            db_s.commit()
            update_job()
        elif now.day > last.day:
            real_user.work_time = now
            real_user.work = None
            db_s.commit()
            update_job()
        elif now.month > last.month:
            real_user.work_time = now
            real_user.work = None
            db_s.commit()
            update_job()
        elif now.year > last.year:
            real_user.work_time = now
            real_user.work = None
            db_s.commit()
            update_job()
    else:
        real_user.work_time = datetime.datetime.today()
        db_s.commit()


def update_vacs():
    db_s = db_session.create_session()
    user = session.get("user").split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    id = int(user[9])
    real_user = db_s.query(User).filter(User.id == id).one()
    if real_user.update_vacs:
        last = real_user.update_vacs
        now = datetime.datetime.now()
        if now - last >= datetime.timedelta(hours=72):
            real_user.update_vacs = now
            db_s.commit()
            return True
        else:
            return False
    else:
        real_user.update_vacs = datetime.datetime.now()
        db_s.commit()


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
                                            data="Только авторизованные пользователи могут пользоваться сервисом"
                                                 " Work At Home"))
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
                user.work_is_done = 0
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
        register_time()
        user = db_sess.query(User).filter(
            User.email == us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')[3]).first()
        return render_template('main.html', data=' '.join([user.name, user.surname]))


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    register_time()
    message = session.get("message_for_job", "")
    db_s = db_session.create_session()
    current = db_s.query(ServerData).one()
    if update_vacs():
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
    d = request.form.get('data')
    d = d.split('"')
    company_name = d[-2]
    c = db_s.query(Jobs).filter(Jobs.name == company_name).one()
    user = session.get("user").split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    if user[11]:
        session["message_for_job"] = 'already'
    else:
        if update_vacs() is False:
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
                        salary = 0
                        for elem in field_head:
                            if str(elem.split('-')[0]) == str(c.id):
                                salary = elem.split('-')[4]
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
                        u.salary = salary
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
    register_time()
    db_s = db_session.create_session()
    us_data = us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    us_id = us_data[9]
    u = db_s.query(User).filter(User.id == int(us_id)).one()
    if u.comp:
        if u.work_is_done == False:
            if not u.work:
                field = u.field
                first, second, third, fourth = '0', '0', '0', '0'
                if field == 'IT':
                    funcs = [['для вывода в консоль', 'print, print()'], ['для перевода данных в строку', 'str, str()'],
                             ['для перевода данных в целое число', 'int, int()'],
                             ['для перевода данных в число с плавающей запятой', 'float, float()'],
                             ['для присваивания значений', '='], ['для перевода данных в список',
                                                                  'list, list(), []'],
                             ['для перевода данных в множество', 'set, set()'],
                             ['для перевода данных в словарь', 'dict, dict(), {}'],
                             'для перевода данных в кортеж', 'tuple, tuple(), ()']
                    ran_first = random.randint(1, 10000)
                    first = f'Чему будет равно число {str(ran_first)} в двоичной системе счисления?'
                    ans_first = str(format(ran_first, 'b'))

                    ran_second = random.randint(1, 10000)
                    second = f'Чему будет равно число {str(ran_second)} в четвертичной системе счисления?'
                    ans_second = ''.join(str(number_to_base(ran_second, 4))[1:-1].split(', '))

                    ran_third = random.randint(1, 10000)
                    third = f'Чему будет равно число {str(ran_third)} в восьмеричной системе счисления?'
                    ans_third = ''.join(str(number_to_base(ran_third, 8))[1:-1].split(', '))

                    ran_fourth = random.choice(funcs)
                    fourth = f'Что служит в Python {ran_fourth[0]}?'
                    ans_fourth = ran_fourth[1].split(', ')

                    print(ans_first, ans_second, ans_third, ans_fourth)

                    f = 'question-answer'.join([first, ans_first])
                    s = 'question-answer'.join([second, ans_second])
                    t = 'question-answer'.join([third, ans_third])
                    ft = 'question-answer'.join([fourth, str(ans_fourth)])
                    user_work = 'between-tasks'.join([f, s, t, ft])
                    u.work = user_work
                    db_s.commit()
                    session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]
                elif field == 'Economics':
                    ran_first = random.randint(20, 80)
                    ran_days_first = random.randint(18, 22)
                    ran_hours_first = random.randint(7, 9)
                    first = f'Сколько денег в конце месяца, в котором {ran_days_first} рабочих дней,' \
                            f' получит работник, который работает {ran_hours_first}' \
                            f' часов в день с зарплатой {ran_first}' \
                            f' д/ч'
                    ans_first = ran_first * ran_hours_first * ran_days_first
                    print(ans_first)

                    ran_second = random.randint(20, 80)
                    ran_days_second = random.randint(18, 22)
                    ran_hours_second = random.randint(7, 9)
                    second = f'Сколько денег в конце месяца, в котором {ran_days_second} рабочих дней,' \
                             f' получит работник, который работает {ran_hours_second}' \
                             f' часов в день с зарплатой {ran_second} д/ч'
                    ans_second = ran_first * ran_hours_second * ran_days_second
                    print(ans_second)

                    ran_third_money = random.choice([5000, 8000, 10000, 6000, 9000, 14000])
                    ran_third_f = random.choice([2, 4, 8])
                    ran_third_s = random.choice([2, 4, 8])
                    third = f'Вам из {ran_third_f} офисов пришло по {ran_third_money} долларов.' \
                            f' По сколько долларов получит каждый из {ran_third_s} других офисов?'
                    ans_third = (ran_third_money * ran_third_f) // ran_third_s
                    print(ans_third)

                    ran_fourth_money = random.choice([50000, 70000, 80000, 90000, 100000, 110000, 120000, 130000])
                    ran_fourth_losses = random.choice([60, 70, 80])
                    fourth = f'Предприятие в среднем зарабатывает {ran_fourth_money} долларов.' \
                             f' Какова будет чистая прибыль в год, если расходы равны {ran_fourth_losses} процентов?'
                    ans_fourth = int((ran_fourth_money * 12) * ((100 - ran_fourth_losses) / 100))
                    print(ans_fourth)

                    f = 'question-answer'.join([first, str(ans_first)])
                    s = 'question-answer'.join([second, str(ans_second)])
                    t = 'question-answer'.join([third, str(ans_third)])
                    ft = 'question-answer'.join([fourth, str(ans_fourth)])

                    user_work = 'between-tasks'.join([f, s, t, ft])
                    u.work = user_work
                    db_s.commit()
                    session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]

                elif field == 'Engineering':
                    ran_first_value = random.randint(500, 2500)
                    ran_first_volume = random.randint(1, 25)
                    first = f'Чему равна масса тела плотности {ran_first_value} кг/куб. метр и ' \
                            f'объема {ran_first_volume} куб. метров?'
                    ans_first = ran_first_value * ran_first_volume

                    second_voltage = 220
                    random_second_current = random.choice([5, 10, 11, 22, 44])
                    second = f'Чему равно сопротивление проводника в сети, напряжение' \
                             f' в которой равно {second_voltage}' \
                             f' вольт, а сила тока равна {random_second_current} ампер?'
                    ans_second = second_voltage // random_second_current

                    third_random_length = random.randint(5, 30)
                    third_random_height = random.randint(5, 15)
                    third_random_radius = random.randint(2, 10)
                    third = f'Чему равна площадь цилиндра (число пи принять за 3), высота боковой' \
                            f' стороны которого равна' \
                            f' {third_random_height} метров, её длина равна {third_random_length} метров,' \
                            f' а радиус основания равен {third_random_radius} метров?'
                    ans_third = (third_random_length * third_random_height) + 2 * (3 * (third_random_radius ** 2))

                    fourth_random_av_speed = random.randint(50, 150)
                    fourth_random_hours = random.randint(2, 15)
                    fourth = f'Какой путь пройдёт автомобиль, двигаясь со средней скоростью {fourth_random_av_speed}' \
                             f' километров в час {fourth_random_hours} часов?'
                    ans_fourth = fourth_random_av_speed * fourth_random_hours

                    f = 'question-answer'.join([first, str(ans_first)])
                    s = 'question-answer'.join([second, str(ans_second)])
                    t = 'question-answer'.join([third, str(ans_third)])
                    ft = 'question-answer'.join([fourth, str(ans_fourth)])

                    user_work = 'between-tasks'.join([f, s, t, ft])
                    u.work = user_work
                    db_s.commit()
                    session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]

            else:
                tasks = u.work.split('between-tasks')
                f = tasks[0]
                s = tasks[1]
                t = tasks[2]
                ft = tasks[3]
                first, ans_first = f.split('question-answer')[0], f.split('question-answer')[1]
                second, ans_second = s.split('question-answer')[0], s.split('question-answer')[1]
                third, ans_third = t.split('question-answer')[0], t.split('question-answer')[1]
                fourth, ans_fourth = ft.split('question-answer')[0], ft.split('question-answer')[1]
                session["answers"] = [ans_first, ans_second, ans_third, ans_fourth]

            return render_template('workwork.html', first=first, second=second, third=third, fourth=fourth)
        else:
            return render_template('workwork.html', done=True)
    else:
        return render_template('workwork.html', message='Вы ещё не работаете в какой-либо компании!')


@app.route('/check_work', methods=['GET', 'POST'])
def check_work():
    form_data = request.form
    answers = session.get("answers", 0)
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    if answers == 0:
        return redirect('/work')
    us_data = us.split('UgandaWillNeverBeChosenAsABioOfSomeoneRight?')
    us_id = us_data[9]
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == int(us_id)).one()
    money = 0
    rate = -2
    max_rate = db_sess.query(Jobs).filter(Jobs.id == int(user.comp)).one().max_rating
    salary = int(user.salary)
    if user.field == 'IT':
        u_first = form_data.get('first')
        u_second = form_data.get('second')
        u_third = form_data.get('third')
        u_fourth = form_data.get('fourth')
        print(answers)
        ans_first, ans_second, ans_third, ans_fourth = answers
        if str(u_first) == ans_first:
            print('1 - OK')
            money += salary
            rate += 1
        else:
            print('1 - NOT OK')
        if str(u_second) == ans_second:
            print('2 - OK')
            money += salary
            rate += 1
        else:
            print('2 - NOT OK')
        if str(u_third) == ans_third:
            print('3 - OK')
            money += salary
            rate += 1
        else:
            print('3 - NOT OK')
        if str(u_fourth) in ans_fourth:
            print('4 - OK')
            money += salary
            rate += 1
        else:
            print('4 - NOT OK')
    elif user.field == 'Economics':
        u_first = form_data.get('first')
        u_second = form_data.get('second')
        u_third = form_data.get('third')
        u_fourth = form_data.get('fourth')
        ans_first, ans_second, ans_third, ans_fourth = answers
        if str(u_first) == str(ans_first):
            print('1 - OK')
            money += salary
            rate += 1
        else:
            print('1 - NOT OK')
        if str(u_second) == str(ans_second):
            print('2 - OK')
            money += salary
            rate += 1
        else:
            print('2 - NOT OK')
        if str(u_third) == str(ans_third):
            print('3 - OK')
            money += salary
            rate += 1
        else:
            print('3 - NOT OK')
        if str(u_fourth) == str(ans_fourth):
            print('4 - OK')
            money += salary
            rate += 1
        else:
            print('4 - NOT OK')
    else:
        u_first = form_data.get('first')
        u_second = form_data.get('second')
        u_third = form_data.get('third')
        u_fourth = form_data.get('fourth')
        ans_first, ans_second, ans_third, ans_fourth = answers
        if str(u_first) == str(ans_first):
            print('1 - OK')
            money += salary
            rate += 1
        else:
            print('1 - NOT OK')
        if str(u_second) == str(ans_second):
            print('2 - OK')
            money += salary
            rate += 1
        else:
            print('2 - NOT OK')
        if str(u_third) == str(ans_third):
            print('3 - OK')
            money += salary
            rate += 1
        else:
            print('3 - NOT OK')
        if str(u_fourth) == str(ans_fourth):
            print('4 - OK')
            money += salary
            rate += 1
        else:
            print('4 - NOT OK')
    user.work = None
    user.work_is_done = True
    user.money += money
    if user.rating + rate >= max_rate:
        user.rating = max_rate
    elif user.rating + rate < 0:
        user.rating = 0
    else:
        user.rating += rate
    db_sess.commit()
    u = db_sess.query(User).filter(User.id == int(us_id)).one()
    data = 'UgandaWillNeverBeChosenAsABioOfSomeoneRight?'.join(
        [u.name, u.surname, str(u.age), u.email, str(u.rating),
         str(u.experience), str(u.money), str(u.mood), u.bio,
         str(u.id), str(u.pfp), ''])
    session["user"] = data
    return redirect('/work')


@app.route('/company')
def company_info():
    us = session.get("user", 0)
    if us == 0:
        return redirect("/login")
    register_time()
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
            usdata.comp = None
            usdata.head = None
            usdata.field = None
            usdata.work_is_done = 0
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
    register_time()
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
