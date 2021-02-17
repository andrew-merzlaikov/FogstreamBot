from django.urls import path
from .views import (UserView,
                    LogicApiView)

app_name = "appserver"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('users', UserView.as_view()),
    path('get/entity/<int:id_user>', LogicApiView.as_view())
]