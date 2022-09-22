import logging
from datetime import datetime

from flask import Flask, render_template, request, redirect, flash, session, url_for, abort
from flask_sqlalchemy import SQLAlchemy

# from blueprints.basic_endpoints import blueprint as basic_endpoints

app = Flask(__name__)
# app.register_blueprint(basic_endpoints)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fgefsfdeg3r23rf5g6h73g'

db = SQLAlchemy(app)


class Statistic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    game = db.Column(db.String(50), nullable=False)
    win_loss = db.Column(db.String(50), nullable=False)
    winning_stat = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/records')
def records():
    statistics = Statistic.query.order_by(Statistic.date.desc()).all()
    return render_template("records.html", statistics=statistics, len=len(statistics))


@app.route('/contact', methods=['POST', "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        name = request.form['username']
        email = request.form['email']
        message = request.form['message']
        print(name + ' ---- ' + email + ' ---- ' + message)
        if len(message) > 0:
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
        return redirect(url_for('user', name=session['userLogged']))
    elif request.method == 'POST' and request.form['login'] == 'selfedu' and request.form['psw'] == '123':
        session['userLogged'] = request.form['login']
        return redirect(url_for('user', name=session['userLogged']))
    return render_template('login.html')


@app.route('/user/<string:name>')
def user(name):
    if 'userLogged' not in session or session['userLogged'] != name:
        abort(401)
    return 'User page: ' + name


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("404.html")


@app.errorhandler(401)
def pageNotFound(error):
    return render_template("401.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
