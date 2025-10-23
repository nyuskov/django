from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["date_of_birth", "photo"]


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "email"]

    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Repeat password"), widget=forms.PasswordInput
    )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Passwords don't match."))
        return cd["password2"]
