# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt
from uuid import uuid4

from sqlalchemy_utils import UUIDType
from flask_login import current_user

from movie_knight.user.models import Role
from movie_knight.database import (
    Column,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
)


class Invitation(SurrogatePK, Model):
    inviter_id = Column(db.Integer, db.ForeignKey('user.id'))
    invitee_id = Column(db.Integer, db.ForeignKey('user.id'))
    code = Column(UUIDType())
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    used_on = Column(db.DateTime, nullable=True)
    expires = Column(db.DateTime, nullable=False)
    invalidated_on = Column(db.DateTime, nullable=True)
    role = Column(db.String(120), nullable=False)

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        self.code = uuid4()
        if self.role is None:
            self.role = "user"

    def valid(self):
        if self.invalidated_on:
            return False
        if self.expires <= dt.datetime.utcnow():
            return False
        if self.invitee_id:
            return False
        return True

    def use_invite_code(self):
        if self.valid():
            self.invitee_id = current_user.id
            role = Role.get_by_name(self.role)
            current_user.add_role(role)
            self.used_on = dt.datetime.utcnow()

    def invalidate(self):
        self.invalidated_on = dt.datetime.utcnow()
        db.session.commit()

    def status(self):
        if self.invalidated_on:
            # invalid
            return 'warning'
        if self.expires <= dt.datetime.utcnow():
            # expired
            return 'danger'
        if self.invitee_id is not None:
            # used
            return 'success'
        else:
            # unused
            return 'primary'

    def __repr__(self):
        return "<{code}>".format(code=self.code)
