from django.urls import path
from django.contrib.auth import views
from .views import (ViewMain, 
                    ViewMessage, 
                    ViewQuestion,
                    ViewUser,
                    ViewLogic, 
                    show_logic,
                    show_edit_form_question,
                    show_edit_form_message)


app_name = "appadmin"

urlpatterns = [
    path('main', ViewMain.as_view(), name='main'),
    path('create/question', ViewQuestion.as_view(), name='create_question'),
    path('create/message', ViewMessage.as_view(), name='create_message'),
    
    path('edit/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='edit_message'),
    
    path('delete/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='delete_message'),
    
    path('edit/question/<int:id_question>', 
        ViewQuestion.as_view(), 
        name='edit_question'),

    path('form/edit/question/<int:id_question>',
         show_edit_form_question,
         name="edit_form_question"), 
    
    path('form/edit/message/<int:id_message>',
         show_edit_form_message,
         name="edit_form_message"), 

    path('delete/question/<int:id_question>', 
         ViewQuestion.as_view(), 
         name='delete_question'),
    
    path('delete/logic', ViewLogic.as_view(), name='delete_logic'),
    path('edit/logic', ViewLogic.as_view(), name='edit_logic'),
    path('show/logic', show_logic, name='show_logic'),
   
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('show/users', ViewUser.as_view(), name='show_users'),
    path('create/logic', ViewLogic.as_view(), name='create_logic')
]