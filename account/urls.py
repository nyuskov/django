from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import dashboard


app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", dashboard, name="dashboard"),
]
