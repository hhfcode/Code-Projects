from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flasksite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.user_id}')"

#this one was scrapped
class soughtgps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Longtitude = db.Column(db.Float, unique=False, nullable=False)
    Latitude = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f"Gps('{self.Longtitude}', '{self.Latitude}')"

class emailsos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"emailsos('{self.id}','{self.email}'"

class bikeGps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Latitude = db.Column(db.Float, unique=False, nullable=False)
    Longtitude = db.Column(db.Float, unique=False, nullable=False)
    bike_id = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"bikeGps('{self.Longtitude}', '{self.Latitude}', '{self.bike_id}')"

class gps(db.Model):
    timestamp = db.Column(db.String, nullable=False, primary_key=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return f"gps ('{self.timestamp}', '{self.longitude}', '{self.latitude}')"

class streetandCity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"streetandCity ('{self.street}','{self.city}')"

