# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import datetime as dt

from flask import flash, current_app
from flask_login import current_user

from movie_knight.user.models import Role
from movie_knight.invitation.models import Invitation
from movie_knight.extensions import db


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}".format(getattr(form, field).label.text, error), category)


def save_profile(user, details, *args, **kwargs):
    if user is not None:
        user.profileurl = details['player']['profileurl']
        user.avatarsmall = details['player']['avatar']
        user.avatarfull = details['player']['avatarfull']
        user.avatarmedium = details['player']['avatarmedium']
        user.steam_id = details['player']['steamid']
        user.save()


# used for adding a default role to a user
def add_user_role(user, details, *args, **kwargs):
    user_role = Role.query.filter_by(name='guest').first()
    if user_role not in user.roles:
        user.add_role(user_role)
        db.session.add(user)
        db.session.commit()
        current_app.logger.info("Adding [{role}] to [{user}]".format(role=user_role.name, user=user.id))
