from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    
    
class Post(models.Model):
    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    class Status(models.TextChoices):
        DRAFT = 'DF', _('Draft')
        PUBLISHED = 'PB', _('Published')

    objects = models.Manager()
    published = PublishedManager()
    title = models.CharField(max_length=250, verbose_name=_('Title'))
    slug = models.SlugField(max_length=250, verbose_name=_('Slug'), unique_for_date='publish')
    body = models.TextField(verbose_name=_('Body'))
    publish = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Published date'),
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created date'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated date'))
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('Status'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name=_('Author'),
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})
    