# # network/permissions.py
# from rest_framework.permissions import BasePermission


# class IsActiveEmployee(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and hasattr(request.user, 'activeemployee') and request.user.activeemployee.is_active
