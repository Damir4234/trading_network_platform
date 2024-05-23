from .serializers import NetworkNodeDetailSerializer, NetworkSerializer
from .models import NetworkNode
from rest_framework.permissions import BasePermission
from rest_framework import viewsets, filters
from network.models import NetworkNode

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'activeemployee') and request.user.activeemployee.is_active


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeDetailSerializer
    permission_classes = [IsAuthenticated, IsActiveEmployee]
    filter_backends = [filters.SearchFilter]
    search_fields = ['country']

    def get_queryset(self):
        network = self.request.query_params.get('network')
        if network:
            return self.queryset.filter(network=network)
        return self.queryset

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save(debt=instance.debt)

    @action(detail=False, methods=['get'])
    def networks(self, request):
        networks = NetworkNode.objects.filter(level=0)
        serializer = NetworkSerializer(networks, many=True)
        return Response(serializer.data)
