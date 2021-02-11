from django.urls import path
from django.contrib.auth import views
from .views import BotView

app_name = "appserver"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('settings', BotView.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]