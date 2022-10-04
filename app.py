import json
import time
from datetime import datetime

import jsonpickle as jsonpickle
from flask import render_template, request, redirect, flash, session, url_for, abort, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fgefsfdeg3r23rf5g6h73g'

db = SQLAlchemy(app)
db.create_all()


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('statistic.user_id'), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    win_loss = db.Column(db.String(50), nullable=False)
    winning_stat = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Stat %r>' % self.id


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    image = db.Column(db.LargeBinary, nullable=True, default=None)


def get_acc(login, psw=None):
    user = Users.query.where(Users.login == login).limit(1)
    if psw and check_password_hash(user[0].password, psw):
        return user[0]
    if not psw and user[0]:
        return user[0]
    return None


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/records')
def records():
    statistics = Statistic.query.order_by(Statistic.date).all()
    return render_template("records.html", statistics=statistics)


@app.route('/contact', methods=['POST', "GET"])
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
    return render_template("contact.html")


@app.route('/add_record', methods=['POST'])
def add_record():
    if request.method == "POST":
        user_id = request.form['user_id']
        game = request.form['game']
        win_loss = request.form['win_loss']
        winning_stat = request.form['winning_stat']
        date = request.form['date']
        stat = Statistic(user_id=user_id, game=game, win_loss=win_loss, winning_stat=winning_stat, date=date)
        try:
            db.session.add(stat)
            db.session.commit()
            return redirect('/')
        except Exception as ex:
            return "Error during saving progress in db: " + ex
    else:
        return render_template("add_record.html")


@app.route('/durak')
def durak():
    return render_template("durak.html")


@app.route('/minesweeper')
def minesweeper():
    return render_template("minesweeper.html")


@app.route('/poker')
def poker():
    return render_template("poker.html")


@app.route('/tic_tac_toe')
def tic_tac_toe():
    return render_template("tic-tac-toe.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('user', user_name=session['login']))
    if request.method == 'POST':
        user = get_acc(request.form['login'], request.form['psw'])
        if user:
            session['login'] = user.login
            session['userLogged'] = jsonpickle.encode(user)
            flash('Success!', category='success')
            return redirect(url_for('user', user_name=session['login']))

        flash('Error! Account not found!', category='error')
    return render_template('login.html')


@app.route('/sign_out')
def sign_out():
    if 'userLogged' in session:
        session.pop('userLogged')
    return redirect('/')


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == 'POST':
        login = request.form['login'].strip()
        password = request.form['psw'].strip()
        password_2 = request.form['psw2'].strip()
        email = request.form['email'].strip()
        if password == password_2:
            info = Users(login=login, password=generate_password_hash(password), email=email)
            try:
                db.session.add(info)
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                if type(ex) == IntegrityError:
                    flash(f'User with this email already exists !!!', category='error')
                    return render_template('registration.html')
                flash(f'Error with database {ex} !!!', category='error')
                return render_template('registration.html')
            flash('Your account has been successfully registered!', category='success')
            session['login'] = info.login
            session['userLogged'] = jsonpickle.encode(info)
            return redirect(url_for('user', user_name=session['login']))
        flash('Error! Passwords dont match!!!', category='error')
    return render_template('registration.html')


@app.route('/user/<string:user_name>')
def user(user_name):
    if 'userLogged' in session:
        user = jsonpickle.decode(session['userLogged'])
        if user.login == user_name:
            return render_template('user.html', user=user)
    abort(401)


@app.errorhandler(404)
def pageNotFound():
    return render_template("404.html")


@app.errorhandler(401)
def noAccess():
    return render_template("401.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
