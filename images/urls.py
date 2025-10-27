from django.urls import path

from .views import ImageCreateView, ImageDetailView

app_name = "images"
urlpatterns = [
    path("create/", ImageCreateView.as_view(), name="create"),
    path(
        "detail/<int:id>/<slug:slug>/", ImageDetailView.as_view(), name="detail"
    ),
]
