from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAdminOrIsSelf(BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff or (obj.user == request.user)
    
        return False