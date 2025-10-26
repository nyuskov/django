from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from .forms import ImageCreateForm


class ImageCreateView(LoginRequiredMixin, FormView):
    form_class = ImageCreateForm
    template_name = "images/image/create.html"

    def post(self, *args, **kwargs):
        # form is sent
        form = self.get_form()
        if form.is_valid():
            # form data is valid
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = self.request.user
            new_image.save()
            messages.success(self.request, _("Image added successfully"))
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())

        context = {"form": form}

        return render(
            self.request,
            self.template_name,
            context,
        )
