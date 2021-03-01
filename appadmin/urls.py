from django.urls import path
from django.contrib.auth import views
from .views import (ViewMain, 
				    ViewMessage,
                    ViewUser,
                    ViewLogic,
                    show_edit_form_message,
					ViewToken,
					ViewMessageDelay,
					show_edit_delay)


app_name = "appadmin"

urlpatterns = [
    path('main', ViewMain.as_view(), name='main'),
    path('create/message', ViewMessage.as_view(), name='create_message'),
	path('delay/get', ViewMessageDelay.as_view(), name="delay_get"),
	path('delat/get/edit/<int:id_message>', show_edit_delay, name="delay_edit_get"),

    path('edit/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='edit_message'),
    
    path('delete/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='delete_message'),
    
    path('form/edit/message/<int:id_message>',
         show_edit_form_message,
         name="edit_form_message"), 

    path('create/form/logic', ViewLogic.as_view(), name="create_form_logic"),
    path('create/logic', ViewLogic.as_view(), name='create_logic'),
    path('delete/logic', ViewLogic.as_view(), name='delete_logic'),

	path('token', ViewToken.as_view(), name='token_get'),
	path('token/set', ViewToken.as_view(), name="token_set"),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('show/users', ViewUser.as_view(), name='show_users')
]