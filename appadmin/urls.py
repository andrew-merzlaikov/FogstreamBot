from django.urls import path
from django.contrib.auth import views
from .views import (ViewMain, 
                    ViewMessage, 
                    ViewQuestion,
                    ViewUser,
                    ViewLogic, 
                    show_logic)


app_name = "appadmin"

urlpatterns = [
    path('main', ViewMain.as_view(), name='main'),
    path('create/question', ViewQuestion.as_view(), name='create_question'),
    path('create/message', ViewMessage.as_view(), name='create_message'),
    path('show/logic', show_logic, name='show_logic'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('show/users', ViewUser.as_view(), name='show_users'),
    path('create/logic', ViewLogic.as_view(), name='create_logic')
]