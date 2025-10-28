from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.models import Action
from actions.utils import create_action


User = get_user_model()


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, "account/user/list.html", {"users": users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "account/user/detail.html", {"user": user})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions.select_related("user", "user__profile").prefetch_related("target")[
        :10
    ]
    context = {"actions": actions}

    return render(request, "account/dashboard.html", context)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            # add action
            create_action(new_user, _("has created an account"))

            return render(
                request, "account/register_done.html", {"new_user": new_user}
            )
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated successfully"))
        else:
            messages.error(request, _("Error updating your profile"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(
                    user_from=request.user, user_to=user
                )
                # add action
                create_action(request.user, _("is following"), user)
            else:
                Contact.objects.filter(
                    user_from=request.user, user_to=user
                ).delete()
            return JsonResponse({"status": "ok"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error"})
    return JsonResponse({"status": "error"})
