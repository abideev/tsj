from flask_login import login_manager
from werkzeug.security import generate_password_hash

from app import db
from datetime import datetime
from slugify import slugify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from random import randint

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(150),  nullable=False)
    surname = db.Column(db.String(150),  nullable=False)
    patronymic = db.Column(db.String(150))
    house_number = db.Column(db.String(50))
    apartment_number = db.Column(db.String(50))
    personal_account_number = db.Column(db.String(50))
    quantity_citizens_registered_at = db.Column(db.String(50))
    type_property = db.Column(db.String(150))
    street=db.Column(db.String(255))
    total_area_premises = db.Column(db.String(50))
    phone = db.Column(db.String(40))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    intercom=db.Column(db.Boolean())
    barrier_count=db.Column(db.String(20))
    image_file=db.Column(db.String(60), default='default.jpg')
    confirmed=db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on=db.Column(db.DateTime, nullable=True)
    accept_licence_policy = db.Column(db.Boolean())
    roles = db.relationship('role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.login

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"



class services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255),  nullable=False)
    description = db.Column(db.String(255),  nullable=False)
    payment = db.Column(db.String(50),  nullable=False)



class news(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240),unique=True, nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(100))
    images = db.Column(db.String(255))
    author = db.Column(db.String(50))
    slug = db.Column(db.String(150),  unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(news, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    # def __repr__(self):
    #     return self.title


def random_integer():
    min_=100
    max_=1000000000
    rand=randint(min_, max_)

    while appeal.query.filter_by(uid=rand).first() is not None:
        rand=randint(min_, max_)

    return rand


class appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(240), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(240),default="отправлено", nullable=True)
    uid = db.Column(db.String(150), default=random_integer, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('user', backref=db.backref('appeal', lazy='dynamic'))


class contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(255),  nullable=False)
    legal_address = db.Column(db.String(255),  nullable=False)
    actual_address = db.Column(db.String(255),  nullable=False)
    email = db.Column(db.String(50),  nullable=False)


class government(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)
    surname = db.Column(db.String(100),  nullable=False)
    patronymic = db.Column(db.String(100),  nullable=False)
    position = db.Column(db.String(150),  nullable=False)
    email = db.Column(db.String(50),  nullable=False)
    phone = db.Column(db.String(20),  nullable=False)


# @login_manager.user_loader
# def load_user(user_id):
#         return user.query.get(user_id)


db.create_all()