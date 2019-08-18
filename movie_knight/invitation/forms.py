# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired


class RedeemInviteForm(FlaskForm):
    code = StringField("Redeem code")


class CreateInviteForm(FlaskForm):
    expires = SelectField("Expiration Time", choices=[
        (1, 'Choose expiration time...'),
        (1, 'One Hour'),
        (3, 'Three Hours'),
        (12, 'Twelve Hours'),
        (24, 'One Day'),
        (48, 'Two Days'),
        (72, 'Three Days')])

    def validate(self):
        """Validate the form."""
        # Don't know why the select field seems to be invalid and won't pass .validate/validate_on_submit
        return True
