from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from rest.functions.UserLogin import UserLogin
from rest.functions.forms import LoginForm, RegistrationForm
from rest.models.db_classes import Statistic, Users, db

main_page = Blueprint('main_page', __name__, template_folder='templates', static_folder='static')


def user_is_logged():
    return current_user.user if current_user.is_authenticated else None


@main_page.route('/')
def index():
    return render_template("main_page/index.html", user=user_is_logged())


@main_page.route('/about')
def about():
    return render_template("main_page/about.html", user=user_is_logged())


@main_page.route('/records')
def records():
    statistics = Statistic.query.order_by(Statistic.date).all()
    return render_template("main_page/records.html", statistics=statistics, user=user_is_logged())


@main_page.route('/contact', methods=['POST', "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        name = request.form['username']
        email = request.form['email']
        message = request.form['message']
        print(name + ' ---- ' + email + ' ---- ' + message)
        if len(message) > 2:
            flash('Message successfully sent!', category='success')
        else:
            flash('Error!', category='error')
    return render_template("main_page/contact.html", user=user_is_logged())


@main_page.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.where(Users.login == form.login.data).limit(1)
        try:
            user = user[0]
        except IndexError as er:
            user = None
        if user and check_password_hash(user.password, form.psw.data):
            user_login = UserLogin().create(user)
            login_user(user_login, remember=form.remember.data)
            flash('Success!', category='success')
            return redirect(url_for('admin.profile'))
        flash('Error! Account not found!', category='error')
    return render_template("main_page/login.html", form=form, user=user_is_logged())


@main_page.route('/registration', methods=["POST", "GET"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.psw1.data
        email = form.email.data
        info = Users(login=login, password=generate_password_hash(password), email=email)
        try:
            db.session.add(info)
            db.session.commit()
            login_user(UserLogin().create(info))
        except Exception as ex:
            db.session.rollback()
            if type(ex) == IntegrityError:
                flash(f'User with this login or email already exists !!!', category='error')
                return render_template('main_page/registration.html', user=user_is_logged())
            flash(f'Error with database {ex} !!!', category='error')
            return render_template('main_page/registration.html', user=user_is_logged())
        flash('Your account has been successfully registered!', category='success')
        return redirect(url_for('admin.profile'))
    return render_template('main_page/registration.html', form=form, user=user_is_logged())


@main_page.route('/sign_out')
def sign_out():
    logout_user()
    flash('Logout successfully!', category='success')
    return redirect('/')



