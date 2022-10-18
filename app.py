from datetime import datetime

from flask import render_template, request, redirect, flash, url_for, make_response, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from rest.functions.UserLogin import UserLogin
from rest.functions.forms import LoginForm, RegistrationForm
from rest.functions.images import image_is_png

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fgefsfdeg3r23rf5g6h73g'
login_manager = LoginManager(app)
db = SQLAlchemy(app)

MAX_CONTENT_LENGTH = 1024 * 1024


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


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


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


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.where(Users.login == form.login.data).limit(1)
        try:
            user = user[0]
        except IndexError as er:
            user = None
        if user and check_password_hash(user[0].password, form.psw.data):
            user_login = UserLogin().create(user[0])
            login_user(user_login, remember=form.remember.data)
            flash('Success!', category='success')
            return redirect(url_for('profile'))
        flash('Error! Account not found!', category='error')
    return render_template("login.html", form=form)


@app.route('/sign_out')
def sign_out():
    logout_user()
    flash('Logout successfully!', category='success')
    return redirect('/')


@app.route('/registration', methods=["POST", "GET"])
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
                return render_template('registration.html')
            flash(f'Error with database {ex} !!!', category='error')
            return render_template('registration.html')
        flash('Your account has been successfully registered!', category='success')
        return redirect(url_for('profile'))
    return render_template('registration.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.user)


@app.route('/userava')
@login_required
def userava():
    img = current_user.get_user_image(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file = image_is_png(file, app)
            if file:
                res = update_user(image=file)
                if res:
                    flash("Success!", "success")
                    return redirect(url_for('profile'))
                flash("Error while updating user image!" "error")
            else:
                flash("Error while reading image file!" "error")
        else:
            flash("No new file for update!" "error")

    return redirect(url_for('profile'))


@app.errorhandler(404)
def pageNotFound():
    return render_template("404.html")


@app.errorhandler(401)
def noAccess():
    return render_template("401.html")


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


def update_user(login=None, psw=None, email=None, image=None):
    user = current_user.user
    if login:
        user.login = login
    if psw:
        user.password = psw
    if email:
        user.email = email
    if image:
        user.image = image
    try:
        db.session.commit()
        login_user.user = user
    except Exception as ex:
        db.session.rollback()
        if type(ex) == IntegrityError:
            flash(f'User with this login or email already exists !!!', category='error')
            return False
        flash(f'Error with database {ex} !!!', category='error')
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
