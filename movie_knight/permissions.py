from permission import Permission

from movie_knight.rules import IsAuthenticated, UserRule, AdminRule


class Template(Permission):
    """Template"""
    def rule(self):
        pass


class AuthenticatedPermission(Permission):
    """Check if a user is authenticated without checking a role."""
    def rule(self):
        return IsAuthenticated()


class UserPermission(Permission):
    """User is authenticated."""
    def rule(self):
        return UserRule()


class AdminPermission(Permission):
    """User is admin."""
    def rule(self):
        return AdminRule()
