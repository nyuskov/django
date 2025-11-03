from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore
from .views import NotificationViewSet, UserNotificationSettingsViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")
router.register(
    r"notification-settings",
    UserNotificationSettingsViewSet,
    basename="notification-settings",
)

app_name = "notifications"

urlpatterns = [
    path("", include(router.urls)),
]
