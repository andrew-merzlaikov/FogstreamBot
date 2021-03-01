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

    # @staticmethod
    # def check_id_parent_bidirectionality(modelformset_message):
    #     """
    #     Функция проверяет не ссылается ли потомок на
    #     родителя
    #     """
        
    #     list_from_new_messages = list()

    #     for form in modelformset_message:
    #         message = form.cleaned_data['id']
    #         list_from_new_messages.append(message)
        
    #     for i in range(0, len(list_from_new_messages)):
    #         id_message = list_from_new_messages[i].id
    #         id_parent_message = list_from_new_messages[i].\
    #                             id_parent

    #         print("ID_MESSAGE", id_message)
    #         print("ID_PARENT_MESSAGE", id_parent_message)

    #         for j in range(i + 1, len(list_from_new_messages)):
    #             id_second_message = list_from_new_messages[j].id
    #             id_parent_second_message = list_from_new_messages[j].\
    #                                        id_parent

    #             print("ID_SECOND_MESSAGE", id_second_message)
    #             print("ID_PARENT_SECOND_MESSAGE", id_parent_second_message)

    #             if (id_message == id_parent_second_message and
    #                 id_parent_message == id_second_message):
    #                 return False

    #     return True

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
