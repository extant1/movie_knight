# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import datetime as dt
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from sqlalchemy import and_

from movie_knight.extensions import login_manager, db
from movie_knight.user.models import User
from movie_knight.invitation.models import Invitation
from movie_knight.invitation.forms import RedeemInviteForm, CreateInviteForm
from movie_knight.permissions import UserPermission

blueprint = Blueprint("invite", __name__, static_folder="../static", url_prefix='/invite')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/redeem', methods=['POST'])
@UserPermission()
def redeem():
    form = RedeemInviteForm()
    if form.validate_on_submit():
        code = form.code.data.lower()
        invitation = Invitation.query.filter_by(code=code).first()
        invitation.use_invite_code()
        flash('You have been assigned the role {role}.'.format(role=invitation.role), category='info')
    return redirect(url_for('public.home'))


@blueprint.route('/manage', methods=['GET'])
@UserPermission()
def manage():
    form = CreateInviteForm()
    now = dt.datetime.utcnow()
    invitations = Invitation.query.filter_by(inviter_id=current_user.id).filter_by(invalidated_on=None).order_by(
        Invitation.expires.desc()).all()
    return render_template('invite/manage.html', invitations=invitations, now=now, form=form)


@blueprint.route('/create', methods=['POST'])
@UserPermission()
def create():
    form = CreateInviteForm()
    if form.validate_on_submit():
        Invitation.create(inviter_id=current_user.id,
                          expires=(dt.datetime.utcnow() + dt.timedelta(hours=int(form.expires.data))),
                          role='user')
    return redirect(url_for('invite.manage'))


@blueprint.route('/invalidate/<int:invitation_id>', methods=['GET'])
@UserPermission()
def invalidate(invitation_id):
    invite = Invitation.query.filter_by(id=invitation_id).first()
    invite.update(invalidated_on=dt.datetime.utcnow())
    return redirect(url_for('invite.manage'))
