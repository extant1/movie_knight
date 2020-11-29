# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys

from flask import Flask, render_template, g
from social_flask.routes import social_auth
from social_flask_sqlalchemy.models import init_social
from flask_login import current_user

from movie_knight import commands, public, user, permissions, backend, invitation
from movie_knight.extensions import (
    moment,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
    flask_static_digest,
)


def create_app(config_object="movie_knight.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    register_context_processors(app)
    register_before_requests(app)
    register_teardown_appcontext(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    moment.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    init_social(app, db.session)
    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(backend.views.blueprint)
    app.register_blueprint(invitation.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(social_auth)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            "User": user.models.User,
            "Stream": user.models.Stream,
            "Role": user.models.Role,
            "Invitation": invitation.models.Invitation
        }

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.socialdb)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)


def register_context_processors(app):
    """Register context_processor functions."""

    @app.context_processor
    def inject_user():
        try:
            return {'user': g.user}
        except AttributeError:
            return {'user': None}

    @app.context_processor
    def inject_var():
        return dict(
            permissions=permissions
        )


def register_teardown_appcontext(app):
    """Register teardown_appcontext functions."""

    def commit_on_success(error=None):
        if error is None:
            db.session.commit()
        else:
            db.session.rollback()

        db.session.remove()

    app.teardown_appcontext(commit_on_success)


def register_before_requests(app):
    """Register before_request functions."""

    def global_user():
        g.user = current_user

    app.before_request(global_user)
