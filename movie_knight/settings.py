# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_BINDS = {
    'users': env.str("SQLALCHEMY_BINDS_USERS")
}
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False
CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.
SQLALCHEMY_TRACK_MODIFICATIONS = False
WEBPACK_MANIFEST_PATH = "webpack/manifest.json"

# Social Auth Base
SOCIAL_AUTH_LOGIN_URL = '/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_USER_MODEL = 'movie_knight.user.models.User'
SOCIAL_AUTH_STORAGE = 'social_flask_sqlalchemy.models.FlaskStorage'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.steam.SteamOpenId',
)
SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']
SOCIAL_AUTH_STEAM_API_KEY = env.str("SOCIAL_AUTH_STEAM_API_KEY")

SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'movie_knight.utils.save_profile',
        # 'movie_knight.utils.add_user_role',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

