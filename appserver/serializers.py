from rest_framework import serializers
from .models import UserTelegram


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_null=True)
    username = serializers.CharField(max_length=30, allow_null=True)

    def create(self, validated_data):
        
        if UserTelegram.objects.filter(username=validated_data['username']).exists():
            return False
        
        return UserTelegram.objects.create(**validated_data)
    