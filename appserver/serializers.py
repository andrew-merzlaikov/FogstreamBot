from rest_framework import serializers
from appadmin.models import UserTelegram
from django.db.models import Q


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_null=True)
    username = serializers.CharField(max_length=30, allow_null=True)
    id_user_telegram = serializers.IntegerField(allow_null=True)

    def create(self, validated_data):

        user_id = validated_data["id_user_telegram"]

        user_exists = UserTelegram.\
                                    objects.\
                                    filter(id_user_telegram=user_id).\
                                    exists()
        if user_exists:
            return False
        
        return UserTelegram.objects.create(**validated_data)

    