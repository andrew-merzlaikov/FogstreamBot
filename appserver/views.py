from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
import json


class UserView(APIView):
    
    def post(self, request):
        
        data_user = json.loads(request.data)['user'] 
        serializer = UserSerializer(data=data_user)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
            return Response({"success": "User '{user_saved}' " 
                                        "created successfully".\
                                        format(user_saved=user_saved)},
                                        content_type="json\application")
        else:
            return Response({"error": "Not valid data"},
                            content_type="json\application")

