# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    abort,
)

from movie_knight.extensions import login_manager, csrf_protect
from movie_knight.user.models import User, Stream
from movie_knight.utils import movie_redirect

blueprint = Blueprint("backend", __name__, static_folder="../static", url_prefix='/backend')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/on_publish/", methods=["POST"])
@csrf_protect.exempt
def on_publish():
    """rtmp on_publish"""

    stream_key = request.form['name']

    stream = Stream.query.filter_by(key=stream_key).first_or_404()

    if not stream.user.active:
        abort(403)
    else:
        stream.live_now()
        # return stream.user.get_name
        return redirect("rtmp://127.0.0.1/hls-live/" + stream.user.get_name, 302)
    abort(403)


@blueprint.route("/on_publish_done/", methods=["POST"])
@csrf_protect.exempt
def on_publish_done():
    """rtmp on_publish_done"""

    stream_key = request.form['name']

    stream = Stream.query.filter_by(key=stream_key).first_or_404()
    stream.finished_stream()
    return redirect(url_for('public.home'))
