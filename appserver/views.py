from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import UserTelegram
from appadmin.models import (Sequence_Logic,
                            User_Sequence_Logic,
                            Message,
                            Question)
from .serializers import UserSerializer
import json
import logging

logger = logging.getLogger(__name__)


class UserView(APIView):
    
    def get(self):
        return Response("TEST")

    def post(self, request):
        
        data_user = json.loads(request.data)['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
            
            logger.debug("TelegramUser '{user_saved}' " 
                                        "created successfully".\
                                        format(user_saved=user_saved))

            return Response({"success": "TelegramUser '{user_saved}' " 
                                        "created successfully".\
                                        format(user_saved=user_saved)},
                                        content_type="json\application")
        else:
            logger.debug("Not valid data")
            return Response({"error": "Not valid data"},
                            content_type="json\application")


class LogicApiView(APIView):

    def get(self, request, id_user):

        if UserTelegram.objects.\
                        filter(id=id_user).\
                        exists():

            if not Sequence_Logic.objects.all().exists():
                return Response({"msg": "Логика общения не создана"},
                                content_type="json\application",
                                status=status.HTTP_404_NOT_FOUND)

            if User_Sequence_Logic.objects.\
                                  filter(user_id=id_user).\
                                  exists():
                
                user_squence_logic = User_Sequence_Logic.\
                                     objects.\
                                     filter(
                                            user_id=id_user
                                      ).\
                                     first()

                id_record = user_squence_logic.next_entity(id_user)

                if Sequence_Logic.objects.filter(id=id_record).exists():
                
                    squence_logic = Sequence_Logic.\
                                                objects.\
                                                filter(id=id_record).\
                                                first()
                    
                    message = Message.objects.\
                                            filter(id=squence_logic.message_id).\
                                            first()

                    question = Question.objects.\
                                                filter(id=squence_logic.question_id).\
                                                first()
                    
                    return Response({"message": str(message),
                                    "message_id": squence_logic.message_id, 
                                    "question": str(question),
                                    "question_id": squence_logic.question_id
                                    },
                                    content_type="json\application")  
                else:
                    return Response({"msg": "Конец логики"},
                                    content_type="json\application",
                                    status=status.HTTP_404_NOT_FOUND)

            else:   
                squence_logic = Sequence_Logic.objects.first()

                user_telegram = UserTelegram.\
                                objects.\
                                filter(id=id_user).\
                                first()

                squence_logic_user = User_Sequence_Logic.\
                                     objects.\
                                     create(
                                            user_id=user_telegram.id,
                                            number_record_logic_id=squence_logic.id)
               
                squence_logic = Sequence_Logic.\
                                objects.\
                                filter(id=squence_logic_user.\
                                      number_record_logic_id).\
                                first()

                message = Message.\
                          objects.\
                          filter(id=squence_logic.message_id).\
                          first()

                question = Question.\
                           objects.\
                           filter(id=squence_logic.question_id).\
                           first()

                return Response({"message": str(message),
                                 "message_id": squence_logic.message_id, 
                                 "question": str(question),
                                 "question_id": squence_logic.question_id
                                },
                                content_type="json\application")
        else:
            return Response({"msg": "Нет пользователя с таким id"},
                            content_type="json\application",
                            status=status.HTTP_404_NOT_FOUND)

