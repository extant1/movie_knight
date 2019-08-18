from flask import flash, redirect, url_for
from flask_login import current_user
from permission import Rule

from movie_knight.user.models import User, Role


class Template(Rule):
    """Template"""
    def check(self):
        pass

    def deny(self):
        pass


class IsAuthenticated(Rule):
    """Check if current_user is authenticated."""
    def check(self):
        return current_user.is_authenticated

    def deny(self):
        flash('You must be logged in.', 'warning')
        return redirect(url_for('public.home'))


class UserRule(Rule):
    """Check if current_user has role 'user'."""
    def base(self):
        return IsAuthenticated()

    def check(self):
        user = Role.get_by_name('user')
        return user in current_user.roles

    def deny(self):
        flash('You do not have appropriate permissions.', 'warning')
        return redirect(url_for('public.home'))


class AdminRule(Rule):
    """Check if current_user has role 'admin'."""
    def base(self):
        return IsAuthenticated()

    def check(self):
        admin = Role.get_by_name('admin')
        return admin in current_user.roles

    def deny(self):
        return redirect(url_for('public.home'))
