from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserTelegram
import json
from .serializers import UserSerializer
from appadmin.models import (Message,
                             TokenBot,
                             MessageDelay,
                             AnswerUser)
from .serializers import UserSerializer
from django.db.models import Q
import json
import logging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

logger = logging.getLogger(__name__)


@api_view(('GET', ))
def get_delay_for_message(request, id_message):

    exists_delay = MessageDelay.\
                   objects.\
                   filter(message_id=id_message).\
                   exists()

    if exists_delay:
        message = MessageDelay.\
                  objects.\
                  filter(message_id=id_message).\
                  get()

        return Response({"delay": message.delay},
                        content_type="json\application")
    else:
        return Response({"delay": 0}, 
                        content_type="json\application")

@api_view(('GET', ))
def count_childs(request, id_current_message):
    count = Message.\
            objects.\
            filter(id_parent=id_current_message).\
            count()
    
    return Response({"count": count}, 
                    content_type="json\application")

@api_view(('GET', ))
def check_end_tree(request, id_current_message):

    check_end_tree = Message.\
                     objects.\
                     filter(id_parent=id_current_message).\
                     exists()
    
    return Response({"exists": check_end_tree})

@api_view(('POST', ))
def set_answer_user(request, id_user_telegram):
    answer = request.POST['answer']
    id_message = request.POST['id_message']
    
    answer = AnswerUser.\
             objects.\
             update_or_create(telegram_user_id=id_user_telegram,
                              message_id=id_message, 
                              defaults={
                                "answer": answer
                              })
    
                              
    return Response({"status": True})

@api_view(('GET', ))
def get_options_answers(request, id_current_message):
    
    messages = Message.\
                      objects.\
                      filter(id_parent=id_current_message).\
                      all()
    
    options_answer = list()

    for message in messages:
        if message is not None:
            if message.display_condition is not None:
                options_answer.append(message.display_condition)


    if options_answer:
        return Response({"options_answer": options_answer},
                        content_type="json\application")
    else:
        return Response({"options_answer": None},
                        content_type="json\application")

@api_view(('GET', ))
def get_token_bot(request):
    token = TokenBot.objects.first()

    return Response({"token": str(token)}, 
                    content_type="json\application")


class UserView(APIView):

    def post(self, request):        
        data_user = request.data['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid():
            user_saved = serializer.save()

            return Response({"success": "TelegramUser '{user_saved}' " 
                                        "создан успешно".\
                                        format(user_saved=user_saved)},
                             content_type="json\application")
        else:
                        
            return Response({"error": "Не валидные данные"},
                            content_type="json\application")


class MessageView(APIView):

    def get(self, request, id_current_message = 0):
        answer = None
        message = None


        if id_current_message == 0:
            message = Message.\
                      objects.\
                      filter(id_parent=0).\
                      get()

            return Response({"message": {
                                "id": message.id,
                                "text_message": message.text_message,
                                "id_parent": message.id_parent,
                                "display_condition": message.display_condition,
                                "write_answer": message.write_answer
                            }}, content_type="json\application") 

        if 'answer' in request.GET.keys():
            answer = request.GET['answer']


        if answer is not None:
        

            message = Message.\
                    objects.\
                    filter(id_parent=id_current_message).\
                    all()
            
            if message[0].display_condition is not None:
                message = Message.\
                          objects.\
                            filter(id_parent=id_current_message).\
                            filter(display_condition=answer).\
                            get()
            else:
                message = Message.\
                          objects.\
                          filter(id_parent=id_current_message).\
                          get()

        else:
            message = Message.\
                      objects.\
                      filter(id_parent=id_current_message).\
                      get()

        return Response({"message": {
                            "id": message.id,
                            "text_message": message.text_message,
                            "id_parent": message.id_parent,
                            "display_condition": message.display_condition,
                            "write_answer": message.write_answer
                        }}, content_type="json\application") 

