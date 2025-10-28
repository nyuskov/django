import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action

# connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                # add action
                create_action(request.user, _("likes"), image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


class ImageRankingView(LoginRequiredMixin, TemplateView):
    template_name = "images/image/ranking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        image_ranking = r.zrange("image_ranking", 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        # get most viewed images
        most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

        context["most_viewed"] = most_viewed
        return context


class ImageCreateView(LoginRequiredMixin, FormView):
    form_class = ImageCreateForm
    template_name = "images/image/create.html"

    def post(self, *args, **kwargs):
        # form is sent
        form = self.get_form()
        try:
            if form.is_valid():
                # form data is valid
                new_image = form.save(commit=False)
                # assign current user to the item
                new_image.user = self.request.user
                new_image.save()
                # add action
                create_action(
                    self.request.user, _("bookmarked image"), new_image
                )
                messages.success(self.request, _("Image added successfully"))
                # redirect to new created item detail view
                return redirect(new_image.get_absolute_url())
        except ValidationError as e:
            messages.error(self.request, e.message)

        context = {"form": form}

        return render(
            self.request,
            self.template_name,
            context,
        )


class ImageDetailView(LoginRequiredMixin, TemplateView):
    template_name = "images/image/detail.html"

    def get(self, *args, **kwargs):
        image_id = kwargs.get("id")
        image_slug = kwargs.get("slug")
        image = get_object_or_404(Image, id=image_id, slug=image_slug)
        # increment total image views by 1
        total_views = r.incr(f"image:{image.id}:views")
        # increment image ranking by 1
        r.zincrby("image_ranking", 1, image.id)

        context = {"image": image, "total_views": total_views}

        return render(
            self.request,
            self.template_name,
            context,
        )


class ImageListView(LoginRequiredMixin, TemplateView):
    template_name = "images/image/list.html"

    def get(self, *args, **kwargs):
        images = Image.objects.all()
        paginator = Paginator(images, 8)
        page = self.request.GET.get("page")
        images_only = self.request.GET.get("images_only")
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            images = paginator.page(1)
        except EmptyPage:
            if images_only:
                # If AJAX request and page out of range
                # return an empty page
                return HttpResponse("")
            # If page out of range return last page of results
            images = paginator.page(paginator.num_pages)

        context = {"images": images}
        if images_only:
            return render(
                self.request,
                "images/image/list_images.html",
                context,
            )
        return render(
            self.request,
            self.template_name,
            context,
        )
