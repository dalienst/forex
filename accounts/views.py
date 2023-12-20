import requests
import base64
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.conf import settings

from accounts.models import Client, Admin
from accounts.forms import ClientCreationForm, AdminCreationForm
from investments.models import InvestCategory, PaymentMethod, Package

User = get_user_model()


@login_required
def dashboard(request):
    investcategory = InvestCategory.objects.all()
    paymentmethods = PaymentMethod.objects.all()
    user_packages = Package.objects.filter(user=request.user)
    user_profile = Client.objects.filter(user=request.user)
    return render(
        request,
        "accounts/dashboard.html",
        {
            "investcategory": investcategory,
            "paymentmethods": paymentmethods,
            "user_packages": user_packages,
            "user_profile": user_profile,
        },
    )


class UserListView(UserPassesTestMixin, ListView):
    """admin sees all users"""

    model = User
    template_name = "users_list.html"
    paginate_by = 6

    def test_func(self):
        return self.request.user.is_staff


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "accounts/user_detail.html"

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)


class ClientSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = ClientCreationForm
    template_name = "registration/signup_form.html"
    success_message = "Account Created Successfully"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "client"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("accounts:dashboard")


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "accounts/user_profile.html"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ClientUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Client
    fields = ["image"]
    template_name = "accounts/user_update.html"
    success_message = "Profile Updated Successfully!"

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:client-profile", kwargs={"pk": self.object.pk})


class AdminSignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = AdminCreationForm
    template_name = "registration/signup_form.html"
    success_message = "Account Created Successfully"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "admin"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("accounts:dashboard")


class AdminDetailView(LoginRequiredMixin, DetailView):
    model = Admin
    template_name = "accounts/user_profile.html"

    def get_queryset(self):
        return Admin.objects.filter(user=self.request.user)


class AdminUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Admin
    fields = ["image"]
    template_name = "accounts/user_update.html"
    success_message = "Profile Updated Successfully!"

    def get_queryset(self):
        return Admin.objects.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("accounts:admin-profile", kwargs={"pk": self.object.pk})
