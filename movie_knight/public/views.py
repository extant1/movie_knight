# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required, logout_user, current_user
from sqlalchemy import and_

from movie_knight.public.forms import NicknameForm
from movie_knight.invitation.forms import RedeemInviteForm
from movie_knight.extensions import login_manager, db
from movie_knight.user.models import User, Stream
from movie_knight.permissions import UserPermission


blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET"])
def home():
    """Home page."""
    form = RedeemInviteForm()
    streams = db.session.query(Stream).join(User).filter(and_(Stream.live_at, User.active)).all()
    return render_template("public/home.html", streams=streams, form=form)


@blueprint.route("/settings", methods=["GET", "POST"])
@UserPermission()
def settings():
    form = NicknameForm()
    if form.validate_on_submit():
        if form.nickname.data is '' or form.nickname.data is None:
            current_user.nickname = None
        current_user.nickname = form.nickname.data
    return render_template("public/settings.html", form=form)


@blueprint.route("/settings/get-key", methods=["GET"])
@UserPermission()
def set_key():
    current_user.stream.change_stream_key()
    return redirect(url_for('public.settings'))


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/<username>", methods=["GET"])
@UserPermission()
def stream(username):
    stream_info = User.get_by_name(username)
    return render_template("public/stream.html", username=username, stream=stream_info)
