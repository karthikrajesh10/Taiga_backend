from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        # Superuser bypass
        if request.user.is_superuser:
            return True

        # return getattr(request.user, "role", None) in self.allowed_roles

        # check primary role in User table
        if request.user.role in self.allowed_roles:
            return True

        # check additional roles in UserRoles table
        return request.user.user_roles.filter(
            role__in=self.allowed_roles
        ).exists()


class IsPM(HasRole):
    allowed_roles = ["PM"]


class IsManager(HasRole):
    allowed_roles = ["MGR"]


class IsDeveloper(HasRole):
    allowed_roles = ["DEV"]


class IsQA(HasRole):
    allowed_roles = ["QA"]


class IsTestLead(HasRole):
    allowed_roles = ["TL"]


class IsApprover(HasRole):
    allowed_roles = ["AP"]

class IsPMOrManager(HasRole):
    allowed_roles = ["PM", "MGR"]

class IsManagerorDeveloper(HasRole):
    allowed_roles = ["DEV", "MGR"]

class IsTestLeadorQA(HasRole):
    allowed_roles = ["TL", "QA"]