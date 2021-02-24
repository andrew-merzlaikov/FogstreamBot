from rest_framework import serializers
from .models import UserTelegram
from appadmin.models import (Question,
                             AnswerUser)
from django.db.models import Q


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_null=True)
    username = serializers.CharField(max_length=30, allow_null=True)

    def create(self, validated_data):
        print(validated_data)
        criter_username = Q(username__icontains=validated_data["username"])
        criter_first_name = Q(first_name__icontains=validated_data["first_name"])
        criter_last_name = Q(last_name__icontains=validated_data["last_name"])

        user_exists = UserTelegram.\
                                    objects.\
                                    filter(criter_username &
                                           criter_first_name &
                                           criter_last_name).\
                                    exists()
        if user_exists:
            return False
        
        return UserTelegram.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    answer_text = serializers.CharField(max_length=30, allow_null=True)
    question_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def create(self, validated_data):        
        return AnswerUser.objects.create(**validated_data)
    