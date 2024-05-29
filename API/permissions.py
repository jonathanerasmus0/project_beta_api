from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'admin'

class IsPaidUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'paid'

class IsFreeUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'free'

class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'accountant'
