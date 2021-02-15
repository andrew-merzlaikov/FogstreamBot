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


class Sequence_Logic(models.Model):
    message = models.OneToOneField(Message, 
                                      on_delete=models.CASCADE)
    question = models.OneToOneField(Question, 
                                       on_delete=models.CASCADE)
    
    message.null = True
    question.null = True

    def set_logic_dict(self, array_from_POST):
        array_from_POST = list(array_from_POST)
        array_from_POST.sort(key=lambda x: x[1])

        
        entities_info = list()

        for item_post in array_from_POST:
            if (item_post[0][0:7] == "message" and 
                item_post[1] != ''):
                
                dict_entity = {"type": "message", 
                               "id": item_post[0][-1], 
                               "number": item_post[1]}

                entities_info.append(dict_entity)
            
            if (item_post[0][0:8] == "question" and 
                item_post[1] != ''):

                dict_entity = {"type": "question", 
                               "id": item_post[0][-1], 
                               "number": item_post[1]}

                entities_info.append(dict_entity)
        
        return entities_info
    
    def __str__(self):
        return "{msg} {quest}".format(msg=self.message,
                                      quest=self.question)


class Answers_Users(models.Model):
    question = models.OneToOneField(Question, 
                                    on_delete=models.CASCADE)
    user = models.OneToOneField(UserTelegram, 
                                on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=150)