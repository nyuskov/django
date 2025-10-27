from django.urls import path

from .views import ImageCreateView, ImageDetailView, ImageListView, image_like

app_name = "images"
urlpatterns = [
    path("create/", ImageCreateView.as_view(), name="create"),
    path(
        "detail/<int:id>/<slug:slug>/", ImageDetailView.as_view(), name="detail"
    ),
    path("like/", image_like, name="like"),
    path("", ImageListView.as_view(), name="list"),
]
