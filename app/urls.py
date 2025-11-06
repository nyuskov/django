"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.utils.translation import gettext as _
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

from blog.sitemaps import PostSitemap

sitemaps = {
    "posts": PostSitemap,
}

# Изменение административной части сайта
admin.site.site_header = _("Project administration")
admin.site.site_title = _("Administrative site of project")
admin.site.index_title = _("Site administration")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("blog/", include("blog.urls", namespace="blog")),
    path("account/", include("account.urls", namespace="account")),
    path("images/", include("images.urls", namespace="images")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("payment/", include("payment.urls", namespace="payment")),
    path("coupons/", include("coupons.urls", namespace="coupons")),
    path("shop/", include("shop.urls", namespace="shop")),
    path(
        "notifications/",
        include("notifications.urls", namespace="notifications"),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.STATIC_URL}images/favicon.ico"),
        name="favicon",
    ),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript_catalog"),
    path("__debug__/", include("debug_toolbar.urls")),
]
