from django.db import models
from appserver.models import UserTelegram


class Message(models.Model):
    text_message = models.CharField(max_length=100)
    id_parent = models.IntegerField()
    display_condition = models.CharField(max_length=50)

    id_parent.null = True
    display_condition.null = True

    def __str__(self):  
        return "{text_message}".format(text_message=self.text_message)
        
