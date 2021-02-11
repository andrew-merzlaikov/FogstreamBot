from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserTelegram
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

