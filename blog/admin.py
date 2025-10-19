from django.contrib import admin
from django.utils.translation import gettext as _

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish')

admin.site.register(Post, PostAdmin)
admin.site.site_header = _('Project administration')
admin.site.index_title = _('Site administration')