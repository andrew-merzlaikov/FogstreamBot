from django.db import models
from appserver.models import UserTelegram
from django.forms import modelformset_factory


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
        
        list_from_logic_dict = list()
        

        for index, entity in enumerate(array_from_POST):
            logic_dict = dict()
            
            if "message" in entity[0]:
                logic_dict["type"] = "message"
                list_from_logic_dict.append(logic_dict)
            elif "question" in entity[0]:
                logic_dict["type"] = "question"
                list_from_logic_dict.append(logic_dict)

        
        # new_list = sorted(list_from_logic_dict, key=lambda k: k['order']) 

        print(list_from_logic_dict)

        return list_from_logic_dict
    
    def __str__(self):
        return "{msg} {quest}".format(msg=self.message,
                                      quest=self.question)


class Answers_Users(models.Model):
    question = models.OneToOneField(Question, 
                                    on_delete=models.CASCADE)
    user = models.OneToOneField(UserTelegram, 
                                on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=150)