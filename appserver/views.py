from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserTelegram
import json
from .serializers import UserSerializer
from appadmin.models import Message
from .serializers import UserSerializer
from django.db.models import Q
import json
import logging
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

logger = logging.getLogger(__name__)

@api_view(('GET', ))
def get_root_message(request):
    root_message = Message.\
                           objects.\
                           filter(id_parent=0).\
                           get()
    

    return Response({"message": { 
                        "id": root_message.id,
                        "text_message": root_message.text_message,
                        "id_parent": root_message.id_parent,
                        "display_condition": root_message.display_condition,
                        "write_answer": root_message.write_answer
                    }}, 
                    content_type="json\application")

@api_view(('GET', ))
def check_end_tree(request, id_current_message):

    check_end_tree = Message.\
                     objects.\
                     filter(id_parent=id_current_message).\
                     exists()
    
    return Response({"exists": check_end_tree})

@api_view(('GET', ))
def get_options_answers(request, id_current_message):
    
    messages = Message.\
                      objects.\
                      filter(id_parent=id_current_message).\
                      all()

    print(messages)
    
    options_answer = list()

    for message in messages:
        options_answer.append(message.display_condition)

    return Response({"options_answer": options_answer},
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

    def get(self, request, id_current_message):
        answer = None

        print("ID_CURRENT_MESSAGE: ", id_current_message)

        if 'answer' in request.GET.keys():
            answer = request.GET['answer']

        message = None

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

