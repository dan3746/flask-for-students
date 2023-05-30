from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from api.rest.base import app

db = SQLAlchemy(app)


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


class Books(db.Model):
    book_id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, default='-')
    year = db.Column(db.Integer, default='-')
    user_id = db.Column(db.Integer, nullable=False)
    private = db.Column(db.Integer, nullable=False, default=1)
    book = db.Column(db.LargeBinary, nullable=False)
