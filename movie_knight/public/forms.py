# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class NicknameForm(FlaskForm):
    nickname = StringField("Nickname")
