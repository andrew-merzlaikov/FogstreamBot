from django.db import models
from appserver.models import UserTelegram


class Question(models.Model):
    question_text = models.CharField(max_length=150)

    def __str__(self):
        return "{message_text}".format(message_text=self.message_text)


class MessageInfo(models.Model):
    after_question = models.BooleanField()
    id_question = models.OneToOneField(Question, 
                                       on_delete=models.CASCADE, 
                                       primary_key=True)


class Message(models.Model):
    text_message = models.CharField(max_length=100)


class SequenceMessageQuestion(models.Model):
    message = models.OneToOneField(Message, 
                                      on_delete=models.CASCADE)
    question = models.OneToOneField(Question, 
                                       on_delete=models.CASCADE)
    
    message.null = True
    question.null = True


class AnswersUsers(models.Model):
    question = models.OneToOneField(Question, 
                                    on_delete=models.CASCADE)
    user = models.OneToOneField(UserTelegram, 
                                on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=150)