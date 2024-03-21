from rest_framework import permissions
from .models import DepartmentAccess
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt


class Authenticated(permissions.BasePermission):
    message = "Access denied. User is not Authenticated"

    def has_permission(self, request, view):
        # Check if the user is authenticated
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        return True


class AdminPermission(permissions.BasePermission):
    message = "Access denied. User is not an Admin"

    def has_permission(self, request, view):
        # Check if the user is authenticated
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        # Get the account_type of the user
        account_type = user.account_type.account_type

        # Grant access if account_type is 3 (Admin), deny access if it's 0 (public), 1 (pending officer) or 2 (officer)
        return account_type == 3


class OfficerPermission(permissions.BasePermission):
    message = "Access denied. User is not an Officer or Admin"

    def has_permission(self, request, view):
        # Check if the user is authenticated
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        # Get the account_type of the user
        account_type = user.account_type.account_type

        # Grant access if account_type is 2 (Officer) or 3 (Admin), deny access if it's not
        return account_type in [2, 3]


class DepartmentAccessPermission(permissions.BasePermission):
    message = "Access denied. User does not have permission for the specified department."

    def has_permission(self, request, view):
        # Check if the user is authenticated
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')

        # Get the user
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])
        user_model = get_user_model()
        user = user_model.objects.filter(user_id=payload['user_id']).first()

        # Get the department_id, user_id and account type from the request
        department_id = request.data.get('department_id')
        user_id = user.user_id
        account_type = user.account_type.account_type

        # Check if the user is an admin (3) or has access to the specified department
        return account_type == 3 or self.has_access(user_id, department_id)

    def has_access(self, user_id, department_id):
        # Check if there is a dataset with the given user_id and department_id in the department access table
        return DepartmentAccess.objects.filter(
            officer_id=user_id,
            department_id=department_id
        ).exists()
