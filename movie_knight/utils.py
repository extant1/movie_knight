# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import datetime as dt

from flask import flash, current_app
from werkzeug.utils import escape
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


def movie_redirect(location, code=302, Response=None):
    """Returns a response object (a WSGI application) that, if called,
    redirects the client to the target location. Supported codes are
    301, 302, 303, 305, 307, and 308. 300 is not supported because
    it's not a real redirect and 304 because it's the answer for a
    request with a request with defined If-Modified-Since headers.
    .. versionadded:: 0.6
       The location can now be a unicode string that is encoded using
       the :func:`iri_to_uri` function.
    .. versionadded:: 0.10
        The class used for the Response object can now be passed in.
    :param location: the location the response should redirect to.
    :param code: the redirect status code. defaults to 302.
    :param class Response: a Response class to use when instantiating a
        response. The default is :class:`werkzeug.wrappers.Response` if
        unspecified.
    """
    if Response is None:
        from werkzeug.wrappers import Response

    response = Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
        "<title>Redirecting...</title>\n"
        "<h1>Redirecting...</h1>\n"
        "<p>You should be redirected automatically to target URL: "
        '<a href="%s">%s</a>.  If not click the link.'
        % (escape(location)),
        code,
        mimetype="text/html",
    )
    response.headers["Location"] = location
    return response
