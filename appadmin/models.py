from django.db import models
from appserver.models import UserTelegram


class TokenBot(models.Model):
    token_bot = models.CharField(max_length=500)

    def __str__(self):
        return "{token_bot}".format(token_bot=self.token_bot)


class Message(models.Model):
    text_message = models.CharField(max_length=500)

    id_parent = models.IntegerField(null=True)

    display_condition = models.CharField(max_length=50, 
                                         null=True, 
                                         blank=True)

    write_answer = models.BooleanField(blank=True,
                                       null=True)

    def __str__(self):  
        return "{text_message}".format(text_message=self.text_message)


class MessageDelay(models.Model):
    message = models.OneToOneField(Message, 
                                   on_delete=models.CASCADE, 
                                   primary_key=True)
    delay = models.IntegerField()


class AnswerUser(models.Model):
    telegram_user = models.ForeignKey(UserTelegram, 
                                      on_delete=models.CASCADE)
    
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE)
    
    answer = models.CharField(max_length=100)