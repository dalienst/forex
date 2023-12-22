from datetime import datetime
import json
from typing import Any
from uuid import UUID
import requests
import base64
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    UpdateView,
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
    Deposit,
    Package,
    PackagePayment,
    PackageWallet,
)
from investments.forms import (
    InvestCategoryForm,
    PackageForm,
    PackagePaymentForm,
)
from forexapp.settings import (
    SHORTCODE,
    TRANSACTION_TYPE,
    CALLBACK_URL,
    PASS_KEY,
    CONSUMER_KEY,
    CONSUMER_SECRET,
)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (UUID,)):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)


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

        # Check if the user already has a package for the selected category
        category = form.cleaned_data["category"]
        existing_package = Package.objects.filter(
            user=self.request.user, category=category
        ).exists()

        if existing_package:
            # If the user already has a package for the selected category, display an error
            messages.error(self.request, f"You already have a {category}.")
            return self.form_invalid(form)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the package information
        user_package = self.get_object()

        # Pass the package information to the form
        payment_form = PackagePaymentForm(initial={"package": user_package})

        # Serialize the user package data if needed
        serialized_data = serialize("json", [user_package], cls=CustomJSONEncoder)

        package_wallet = PackageWallet.objects.get(package=user_package)

        # Add the form and serialized data to the context
        context["package_wallet"] = package_wallet
        context["payment_form"] = payment_form
        context["package_data_json"] = serialized_data

        return context

    def get_success_url(self):
        return reverse_lazy("investments:package-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        payment_form = PackagePaymentForm(request.POST)
        if payment_form.is_valid():
            package = self.object
            user = self.request.user
            phone_number = request.POST.get("phone_number")
            receipt = request.POST.get("receipt")

            PackagePayment.objects.create(
                user=user,
                package=package,
                receipt=receipt,
                phone_number=phone_number,
            )

            messages.success(
                request,
                "Payment Confirmation Received. Package will be updated shortly",
            )

            return redirect(self.get_success_url())
        messages.error(request, "Error in payment confirmation form.")

        # Use super() to get the context and add the payment_form to it
        context = self.get_context_data()
        context["payment_form"] = payment_form

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


# create a delete method that deletes the package after 7 days or moves to trash model


# class PackageWalletDetail(LoginRequiredMixin, DetailView):
#     model = PackageWallet
#     template_name


class DepositResultsView(CreateView):
    def post(self, request, *args, **kwargs):
        try:
            result = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            amount = result[0]["Value"]
            transaction_ref = result[1]["Value"]
            phone = result[3]["Value"]
            timestamp = result[2]["Value"]
            success_code = request.data["Body"]["stkCallback"]["ResultCode"] == 0
        except KeyError as e:
            messages.error(request, f"Invalid callback data. Missing key: {e}")
            return render(request, "error_template.html")
        except (IndexError, TypeError):
            messages.error(request, "Invalid callback data. Unexpected data structure.")
            return render(request, "error_template.html")

        if success_code:
            Deposit.objects.create(
                amount=amount, phone=phone, trans_ref=transaction_ref
            )
            messages.success(request, "Payment processed successfully")
            return render(request, "payment_success_template.html")
        else:
            messages.error(request, "Could not process payment")
            return render(request, "error_template.html")
