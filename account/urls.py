from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path, reverse_lazy, include

from .views import dashboard, register, edit


app_name = "account"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # password change
    path(
        "password_change/",
        PasswordChangeView.as_view(
            success_url=reverse_lazy("account:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    # password reset
    path(
        "password_reset/",
        PasswordResetView.as_view(
            success_url=reverse_lazy("account:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("account:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # path("", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("register", register, name="register"),
    path("edit/", edit, name="edit"),
]
