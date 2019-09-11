# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, DataRequired


class RedeemInviteForm(FlaskForm):
    code = StringField("Redeem code")

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RedeemInviteForm, self).__init__(*args, **kwargs)

    def validate(self):
        """Validate the form."""
        initial_validation = super(RedeemInviteForm, self).validate()
        if not initial_validation:
            return False
        return True


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
        return True
    # def __init__(self, *args, **kwargs):
    #     """Create instance."""
    #     super(CreateInviteForm, self).__init__(*args, **kwargs)
    #
    # def validate(self):
    #     """Validate the form."""
    #     initial_validation = super(CreateInviteForm, self).validate()
    #     print(initial_validation)
    #     if not initial_validation:
    #         return False
    #     print("valid")
    #     return True
