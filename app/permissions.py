from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth.hashers import check_password


class JustAdminPermission(BasePermission):
    def has_permission(self, request: Request, view):
        if request.user.username == 'admin' and check_password('admin', request.user.password):
            return True
        return False