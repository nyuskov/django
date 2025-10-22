import markdown  # type: ignore
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from .models import Post


class LatestPostsFeed(Feed):
    title = _("My blog")
    link = reverse_lazy("blog:post_list")
    description = _("New posts of my blog")

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 100)

    def item_pubdate(self, item):
        return item.publish
