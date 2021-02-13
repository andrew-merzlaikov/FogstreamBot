from django.urls import path
from django.contrib.auth import views
from .views import (ViewMain, 
                    ViewMessage, 
                    ViewQuestion,
                    ViewUser,
                    ViewLogic, 
                    show_logic)

app_name = "appserver"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('settings', ViewMain.as_view()),
    path('message', ViewMessage.as_view()),
    path('question', ViewQuestion.as_view()),
    path('create/message', ViewMessage.as_view()),
    path('show/logic', show_logic),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('users', ViewUser.as_view()),
    path('logic', ViewLogic.as_view())
]