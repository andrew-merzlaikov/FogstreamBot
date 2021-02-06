from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

class UserView(APIView):
    
    def post(self, request):
        user = request.data.get('user')

        serializer = UserSerializer(data=user)

        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
            return Response({"success": "User '{user_saved}' " 
                                        "created successfully".\
                                        format(user_saved=user_saved)},
                                        content_type="json\application")

