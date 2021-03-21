from django.urls import path
from .views import (create_user, 
                    get_next_message,
                    get_options_answers,
                    get_token_bot,
                    get_delay_for_message,
                    set_answer_user,
                    count_childs,
                    set_current_message,
                    get_current_message)

app_name = "appserver"

urlpatterns = [
    path('create/user', create_user),
    path('get/next/message/<int:id_current_message>', get_next_message),
    path('get/options_answers/<int:id_current_message>', get_options_answers),
    path('get/token', get_token_bot),
    path('get/count/child/<int:id_current_message>', count_childs),
    path('get/delay/message/<int:id_message>', get_delay_for_message),
    path('set/answer/<int:id_user_telegram>', set_answer_user),
    path('set/current_message/<int:id_user_telegram>/'
         '<int:id_current_message>', set_current_message),
    path('get/current_message/<int:id_user_telegram>', get_current_message)
]