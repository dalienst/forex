from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy


from investments.models import (
    InvestCategory,
    PaymentMethod,
    Transaction,
    Deposit,
    Withdrawal,
    Package,
)
from investments.forms import (
    InvestCategoryForm,
    DepositForm,
    WithdrawalForm,
    PackageForm,
)
from forexapp.settings import (
    SHORTCODE,
    TRANSACTION_TYPE,
    CALLBACK_URL,
    PASS_KEY,
    CONSUMER_KEY,
    CONSUMER_SECRET,
)


def landing(request):
    packages = InvestCategory.objects.all()
    return render(request, "landing.html", {"packages": packages})


class InvestCategoryCreateView(
    SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    model = InvestCategory
    form_class = InvestCategoryForm
    template_name = "category_create.html"
    success_message = "Investment Category Created"
    success_url = reverse_lazy("accounts:dashboard")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class InvestCategoryListView(ListView):
    model = InvestCategory
    template_name = "category_list.html"


class InvestCategoryDetailView(LoginRequiredMixin, DetailView):
    model = InvestCategory
    template_name = "category_detail.html"


class InvestCategoryUpdateView(
    SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView
):
    model = InvestCategory
    success_message = "Investment Category Updated"
    template_name = "category_list.html"
    success_url = reverse_lazy("accounts:dashboard")

    def test_func(self) -> bool | None:
        return self.request.user.is_superuser


"""
Views specifically for packages start here
Subscribing for packages
"""


@login_required
def portfolio(request):
    paymentmethods = PaymentMethod.objects.all()
    user_packages = Package.objects.filter(user=request.user)
    return render(
        request,
        "portfolio.html",
        {"paymentmethods": paymentmethods, "user_packages": user_packages},
    )


class PackageCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = "package_create.html"
    success_message = "Successfully Subscribed to The Package"
    success_url = reverse_lazy("investments:portfolio")

    def form_valid(self, form):
        # Set the user field to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class PackageListView(LoginRequiredMixin, ListView):
    template_name = "package_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Package.objects.filter(user=self.request.user)


class PackageDetailView(LoginRequiredMixin, DetailView):
    template_name = "package_detail.html"
    context_object_name = "package_detail"

    def get_queryset(self) -> QuerySet[Any]:
        return Package.objects.filter(user=self.request.user)


# create a delete method that deletes the package after 7 days or moves to trash model
