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
        deposit_form = DepositForm(initial={"package": self.object})
        serialized_data = serialize("json", [self.object], cls=CustomJSONEncoder)
        context["deposit_form"] = deposit_form
        context["package_data_json"] = serialized_data
        return context

    def get_success_url(self):
        return reverse_lazy("investments:package-detail", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            user_package = self.object
            amount = deposit_form.cleaned_data["amount"]
            phone = deposit_form.cleaned_data["phone"]

            # validation of amount
            if (
                amount < user_package.category.price
                or amount > user_package.category.max_price
            ):
                messages.error(
                    request,
                    f"Amount should be between {user_package.category.price} and {user_package.category.max_price}",
                )
                return self.render_to_response(
                    self.get_context_data(deposit_form=deposit_form)
                )

            # Get access token
            access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            auth_response = requests.get(
                access_token_url, auth=(CONSUMER_KEY, CONSUMER_SECRET)
            )
            auth_data = auth_response.json()
            access_token = auth_data.get("access_token")

            if not access_token:
                messages.error(request, "Error Processing Payment")
                return render(
                    request,
                    "package_detail.html",
                    {"form": deposit_form},
                )

            # Prepare data for API call
            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            shortcode = str(SHORTCODE)
            passkey = str(PASS_KEY)
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            concatenated = f"{shortcode}{passkey}{timestamp}".encode()
            password = base64.b64encode(concatenated).decode()
            description_transaction = str(user_package)

            payload = {
                "BusinessShortCode": SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": TRANSACTION_TYPE,
                "Amount": amount,
                "PartyA": phone,
                "PartyB": SHORTCODE,
                "PhoneNumber": phone,
                "CallBackURL": CALLBACK_URL,
                "AccountReference": description_transaction,
                "TransactionDesc": description_transaction,
            }

            # Make the API call
            api_response = requests.post(api_url, json=payload, headers=headers)
            response_data = api_response.json()

            messages.success(request, "Please check your phone, payment is processing")

            Deposit.objects.create(
                user=request.user, package=user_package, amount=amount, phone=phone
            )

            return render(
                request,
                "success_template.html",
                {"message": response_data, "form": deposit_form},
            )
            # return redirect(self.get_success_url())
        else:
            messages.error(request, "Error in deposit form.")
            return self.render_to_response(
                self.get_context_data(deposit_form=deposit_form)
            )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)


# create a delete method that deletes the package after 7 days or moves to trash model
