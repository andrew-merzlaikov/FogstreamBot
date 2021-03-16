from django.urls import path
from django.contrib.auth import views
from .views.message_view import (ViewMessage,
                                 set_root_message,
                                 show_edit_form_message)

from .views.token_view import ViewToken
from .views.logic_edit_view import (delete_logic,
                                    get_form_create_logic,
                                    get_table_for_logic)

from .views.main_view import ViewMain
from .views.childs_views import (ViewChilds,
                                 get_childs_message,
                                 get_form_edit_childs)
from .views.message_delay_view import (ViewMessageDelay,
                                       show_edit_delay)
from .views.user_view import (get_info_user,
                              info_users_list)

app_name = "appadmin"

urlpatterns = [
      
    path('main', 
         ViewMain.as_view(), 
         name='main'),
	
    path('delay/get', 
          ViewMessageDelay.as_view(), 
          name="delay_get"),
    
    path('delay/get/edit/<int:id_message>', 
          show_edit_delay, 
          name="delay_edit_get"),
    
    path('delay/set/<int:id_message>', 
          ViewMessageDelay.as_view(), 
          name="delay_set"),
    
    path('delay/delete/<int:id_message>', 
          ViewMessageDelay.as_view(), 
          name="delay_delete"),

    path('show/logic', 
          get_table_for_logic, 
          name="table_for_logic"),
    
    path('create/logic/', 
          get_form_create_logic, 
          name="get_create_logic"),
    path('set/root/message', 
          set_root_message, 
          name="set_root_message"),
    path('show/childs/<int:id_message>', 
          get_childs_message, 
          name="get_childs"),
    
    path('create/childs/<int:id_parent>', 
         ViewChilds.as_view(), 
         name="get_form_create_childs"),
    
    path('set/childs/<int:id_parent>/<int:count_childs>', 
         ViewChilds.as_view(), 
         name="set_form_create_childs"),
    
    path('get/edit/childs/<int:id_parent>', 
         get_form_edit_childs, 
         name="get_form_edit_childs"),
    

    path('show/messages', 
          ViewMessage.as_view(), 
          name="show_messages"),
    path('set/message', 
          ViewMessage.as_view(), 
          name="set_message"),
    path('edit/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='edit_message'),
    path('delete/message/<int:id_message>', 
         ViewMessage.as_view(), 
         name='delete_message'),
    

    path('form/edit/message/<int:id_message>',
         show_edit_form_message,
         name="edit_form_message"), 

    path('show/info/users', 
         info_users_list, 
         name="info_users_list"),
    path('delete/logic', 
         delete_logic, 
         name='delete_logic'),

	path('token', 
          ViewToken.as_view(), 
          name='token_get'),
	path('token/set', 
         ViewToken.as_view(), 
         name="token_set"),

    path('login/', 
          views.LoginView.as_view(), 
          name='login'),

    path('logout/', 
         views.LogoutView.as_view(), 
         name='logout'),
    path('get/info/<int:telegram_user_id>', 
         get_info_user, 
         name="get_info_user")
]