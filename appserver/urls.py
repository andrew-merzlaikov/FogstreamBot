from django.urls import path
from .views import (UserView, 
                    MessageView,
                    get_options_answers,
                    check_end_tree,
                    get_token_bot,
                    get_delay_for_message,
                    set_answer_user)

app_name = "appserver"

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/next/message/<int:id_current_message>', MessageView.as_view()),
    path('get/options_answers/<int:id_current_message>', get_options_answers),
    path('get/check/end_tree/<int:id_current_message>', check_end_tree),
    path('get/token', get_token_bot),
    path('get/delay/message/<int:id_message>', get_delay_for_message),
    path('set/answer/<int:id_user_telegram>', set_answer_user),
]