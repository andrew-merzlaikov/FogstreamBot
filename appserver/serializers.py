from rest_framework import serializers
from .models import UserTelegram
from appadmin.models import (Question,
                             AnswerUser)


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_null=True)
    username = serializers.CharField(max_length=30, allow_null=True)

    def create(self, validated_data):
        
        if UserTelegram.objects.filter(username=validated_data['username']).exists():
            return False
        
        return UserTelegram.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    answer_text = serializers.CharField(max_length=30, allow_null=True)
    question_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):        
        return AnswerUser.objects.create(**validated_data)
    