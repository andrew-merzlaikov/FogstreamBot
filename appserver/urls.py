from django.urls import path
from .views import (UserView,
                    LogicApiView,
                    AnswerView, 
                    get_logic_entity)

app_name = "appserver"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/entity/<int:id_user>', LogicApiView.as_view()),
    path('get/user_id/', UserView.as_view()),
    path('get/count_entities', get_logic_entity),
    path('set/answer', AnswerView.as_view())
]