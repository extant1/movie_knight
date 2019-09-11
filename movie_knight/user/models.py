# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
import random
import os

from flask import request
from flask_login import UserMixin

from movie_knight.words import adjectives, nouns
from movie_knight.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class Role(SurrogatePK, Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(255))
    color = db.Column(db.String(20))
    bgcolor = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_by_name(name):
        return Role.query.filter_by(name=name).first()

    def __repr__(self):
        """Represent instance as a string."""
        return "{name!r}".format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""
    __tablename__ = 'user'

    # required for python-social-auth ¯\_(ツ)_/¯
    email = Column(db.String(100), nullable=True)

    username = Column(db.String(100))
    nickname = Column(db.String(100))
    steam_id = Column(db.String(100))
    avatarfull = Column(db.String(255))
    avatarmedium = Column(db.String(255))
    avatarsmall = Column(db.String(255))
    profileurl = Column(db.String(255))

    roles = db.relationship(
        'Role',
        secondary=user_roles,
        backref=db.backref('roles', lazy='dynamic')
    )

    invitations = db.relationship(
        'Invitation',
        backref='inviter',
        foreign_keys="Invitation.inviter_id"
    )

    invitee = db.relationship(
        'Invitation',
        backref='invitee',
        uselist=False,
        foreign_keys="Invitation.invitee_id"
    )

    last_ip = Column(db.String(100))
    last_login = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    current_login = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    current_ip = Column(db.String(100))

    privacy = Column(db.Boolean(), default=True)

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = Column(db.Boolean(), default=True)

    notes = Column(db.Text)

    stream = db.relationship(
        'Stream',
        backref='user',
        uselist=False
    )

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def track_user(self):
        self.last_ip = self.current_ip
        self.last_login = self.current_login
        self.current_ip = request.access_route[0]
        self.current_login = dt.datetime.utcnow()

    def add_role(self, role):
        self.roles.append(role)
        self.save()

    def add_roles(self, roles):
        for role in roles:
            self.add_role(role)
        self.save()

    def toggle_privacy(self):
        if self.privacy:
            self.privacy = False
        else:
            self.privacy = True

    @property
    def get_name(self):
        if self.nickname is None or self.nickname is '':
            return str(self.username)
        else:
            return str(self.nickname)

    def suspend_user(self):
        self.active = False

    def activate_user(self):
        self.active = True

    @staticmethod
    def get_by_name(name):
        name = User.query.filter_by(username=name).first()
        if name is None:
            User.query.filter_by(nickname=name).first()
        return name

    def __repr__(self):
        return self.get_name


class Stream(SurrogatePK, Model):
    __tablename__ = "stream"
    """Stream model."""

    key = Column(db.String(200))
    live_at = Column(db.DateTime, nullable=True)
    last_live = Column(db.DateTime, nullable=True)
    user_id = Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        if self.key is None:
            self.key = Stream.create_stream_key()

    @staticmethod
    def create_stream_key():
        random.seed = os.urandom(1024)
        adjective_1 = random.choice(adjectives)
        adjective_2 = random.choice(adjectives)
        noun = random.choice(nouns)
        key = '{0}{1}{2}'.format(adjective_1.capitalize(), adjective_2.capitalize(), noun.capitalize())
        key_check = Stream.query.filter_by(key=key).first()

        if key_check is not None:
            Stream.create_stream_key()
        else:
            return key

    def change_stream_key(self):
        self.key = Stream.create_stream_key()

    def live_now(self):
        self.live_at = dt.datetime.utcnow()
        self.last_live = dt.datetime.utcnow()
        db.session.commit()

    def finished_stream(self):
        self.live_at = None
        db.session.commit()

    def __repr__(self):
        # return '{key!r}'.format(key=self.key)
        return '{key!r}'.format(key=self.key)
