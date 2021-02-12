from django.db import models
from appserver.models import UserTelegram


class Question(models.Model):
    
    question = models.CharField(max_length=150)

    question_confirm = models.CharField(max_length=50,
                                        null=True)
    question_not_confirm = models.CharField(max_length=50,
                                            null=True)

    question_confirm.null = True
    question_not_confirm.null = True

    def __str__(self):
        return "{question_text}".format(question_text=self.question)


class Message(models.Model):
    text_message = models.CharField(max_length=100)

    def __str__(self):
        return "{text_message}".format(text_message=self.text_message)


class Message_Question(models.Model):
    message = models.OneToOneField(Message, 
                                      on_delete=models.CASCADE)
    question = models.OneToOneField(Question, 
                                       on_delete=models.CASCADE)
    
    message.null = True
    question.null = True


class Answers_Users(models.Model):
    question = models.OneToOneField(Question, 
                                    on_delete=models.CASCADE)
    user = models.OneToOneField(UserTelegram, 
                                on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=150)