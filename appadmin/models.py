from django.db import models
from appserver.models import UserTelegram


class TokenBot(models.Model):
    token_bot = models.CharField(max_length=500)

    def __str__(self):
        return "{token_bot}".format(token_bot=self.token_bot)


class Message(models.Model):
    text_message = models.CharField(max_length=200)

    id_parent = models.IntegerField(null=True)

    display_condition = models.CharField(max_length=50, 
                                         null=True, 
                                         blank=True)

    write_answer = models.BooleanField(blank=True,
                                       null=True)

    def __str__(self):  
        return "{text_message}".format(text_message=self.text_message)

    @staticmethod
    def check_parent_myself(form_message):

        if (form_message['id_parent'] == form_message['id'].id):
            return {"message": ("Сообщение (" + str(form_message['id']) + 
                                ") не может быть само себе родителем")}
        else:
            return True

    @staticmethod
    def check_message_id_parent(id_parent):
        """
        Функция проверяет есть ли такой родитель в базе 
        данных
        """               

        if id_parent != 0:
            exists_message = Message.\
                            objects.\
                            filter(id=id_parent).\
                            exists()

            if exists_message:
                return True
            else:
                return False
        
        else:
            return True

    @staticmethod
    def check_parent_in_messages(modelformset_message):
        """
        Функция проверяет есть ли родитель в дереве
        """

        for form in modelformset_message:
            id_parent = form.cleaned_data['id_parent']                      
            print(id_parent)

            if id_parent == 0:
                return True
        
        return  False


class MessageDelay(models.Model):
    message = models.OneToOneField(Message, 
                                   on_delete = models.CASCADE, 
                                   primary_key = True)
    delay = models.IntegerField()


# class AnswersUser(models.Model):
#     user = 
