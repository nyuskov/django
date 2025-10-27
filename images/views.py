from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import ImageCreateForm
from .models import Image


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
        context = {"image": image}
        return render(
            self.request,
            self.template_name,
            context,
        )
