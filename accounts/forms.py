from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Client, Admin
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()


class ClientCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_client = True
        user.save()
        Client.objects.create(user=user)
        return user


class AdminCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()
        Admin.objects.create(user=user)
        return user


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "image",
            "phone_number",
            "identification",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].label = "Profile Picture"
        self.fields["phone_number"].label = "Phone Number"
        self.fields["identification"].label = "ID/Passport Number"
