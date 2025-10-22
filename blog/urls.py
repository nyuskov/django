from django.urls import path

from .feeds import LatestPostsFeed
from .views import PostDetailView, PostShareView, PostCommentView, PostListView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        PostDetailView.as_view(),
        name="post_detail",
    ),
    path("<int:post_id>/share/", PostShareView.as_view(), name="post_share"),
    path(
        "<int:post_id>/comment/", PostCommentView.as_view(), name="post_comment"
    ),
    path(
        "tag/<slug:tag_slug>/", PostListView.as_view(), name="post_list_by_tag"
    ),
    path("feed/", LatestPostsFeed(), name="post_feed"),
]
