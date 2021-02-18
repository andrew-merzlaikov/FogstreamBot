from django.urls import path
from .views import (UserView,
                    LogicApiView,
                    AnswerView)

app_name = "appserver"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/entity/<int:id_user>', LogicApiView.as_view()),
    path('get/count_entities', AnswerView.as_view()),
    path('set/answer', AnswerView.as_view())
]