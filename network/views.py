from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from network.models import NetworkNode
from network.serializers import NetworkNodeSerializer


class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'activeemployee') and request.user.activeemployee.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        country = self.request.query_params.get('country')
        if country:
            return self.queryset.filter(country=country)
        return self.queryset
