from rest_framework import serializers
from .models import NetworkNode
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class NetworkNodeDetailSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(
        source='get_level_display', read_only=True)
    supplier_name = serializers.CharField(
        source='supplier.name', read_only=True)
    child_nodes = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'level_display', 'name', 'contact_email', 'country',
            'city', 'street', 'house_number', 'products', 'debt',
            'created_at', 'level', 'network', 'supplier', 'supplier_name',
            'child_nodes'
        ]

    def get_child_nodes(self, obj):
        child_nodes = NetworkNode.objects.filter(supplier=obj)
        return NetworkNodeDetailSerializer(child_nodes, many=True).data


class NetworkSerializer(serializers.ModelSerializer):
    nodes = serializers.SerializerMethodField()

    class Meta:
        model = NetworkNode
        fields = ['id', 'name', 'network', 'nodes']

    def get_nodes(self, obj):
        nodes = NetworkNode.objects.filter(supplier=obj)
        return NetworkNodeDetailSerializer(nodes, many=True).data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = authenticate(
            username=attrs[self.username_field], password=attrs['password'])
        if user and not user.is_active:
            raise serializers.ValidationError("User is not active.")
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
