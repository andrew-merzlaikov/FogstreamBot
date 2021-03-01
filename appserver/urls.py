from django.urls import path
from .views import (UserView, 
                    MessageView,
                    get_root_message,
                    get_options_answers,
                    check_end_tree)

app_name = "appserver"

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/next/message/<int:id_current_message>', MessageView.as_view()),
    path('get/options_answers/<int:id_current_message>', get_options_answers),
    path('get/check/end_tree/<int:id_current_message>', check_end_tree),
    path('get/root/message', get_root_message)
]