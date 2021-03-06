# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from atss4po.database import Column, Model, SurrogatePK, db, reference_col, relationship
from atss4po.extensions import bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from .identicon import Identicon
import time

class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    last_use = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    uploads = Column(db.Integer, nullable=False, default=0)
    use = Column(db.Integer, nullable=False, default=0)
    avatar = Column(db.String(1000), unique=True, nullable=False)
    biography = Column(db.String(1000), default="这家伙很懒，没有介绍")

    def get_today_use(self):
        last_use = self.last_use
        last_use = last_use.strftime('%Y%m%d')
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        if today == last_use:
            use = self.use
        else:
            use = 0
        return use

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        avatar_generator = Identicon(username)
        avatar = avatar_generator.generate()
        db.Model.__init__(self, username=username, email=email, avatar=avatar,**kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def generate_auth_token(self, expiration=360000):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.filter_by(id=data['id']).first()
        return user

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

class Article(SurrogatePK, Model):
    __tablename__ = 'articles'
    filepath = Column(db.String(1000), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    summarized = Column(db.Boolean(), default=False)

    def __init__(self, filepath):
        """Create instance."""
        db.Model.__init__(self, filepath=filepath)
    def __repr__(self):
        return '<Article({filepath})>'.format(filepath=self.filepath)

class SummarizedArticle(SurrogatePK, Model):
    __tablename__ = 'summarized_articles'
    text = Column(db.Text, nullable=False)
    summarization = Column(db.Text, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, text, summarization):
        db.Model.__init__(self, text=text, summarization=summarization)

    def __repr__(self):
        return '<Article()>'
