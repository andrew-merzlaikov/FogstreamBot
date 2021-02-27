from django.db import models
from appserver.models import UserTelegram


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
    def check_id_parent_bidirectionality(id_parent, id_message):
        """
        Функция проверяет не ссылается ли потомок на
        родителя
        """
        
        message_first = Message.objects.\
                        filter(id=id_parent).get()
        
        message_second = Message.objects.\
                         filter(id=id_message).get()

        if (message_first.id == message_second.id_parent and
            message_first.id_parent == message_second.id):
            return False
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

