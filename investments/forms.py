from typing import Any
from django import forms
from django.db import transaction

from investments.models import (
    InvestCategory,
    Deposit,
    Withdrawal,
    Package,
    PackagePayment,
    PackageWallet,
)


class InvestCategoryForm(forms.ModelForm):
    class Meta:
        model = InvestCategory
        fields = [
            "name",
            "description",
            "price",
        ]


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            "category",
        ]

    @transaction.atomic
    def save(self, commit=True) -> Any:
        package = super().save(commit=commit)

        # Create a PackageWallet associated with the saved package
        PackageWallet.objects.create(package=package)

        return package


class PackagePaymentForm(forms.ModelForm):
    class Meta:
        model = PackagePayment
        fields = [
            "receipt",
            "phone_number",
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["receipt_number"].label = "M-PESA Transaction Code"
            self.fields["phone_number"].label = "Phone Number"
            self.fields["package"].widget.attrs["readonly"] = True


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = (
            "amount",
            "phone",
        )
        # widgets = {"package"}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Make the package field read-only
    #     self.fields["package"].widget.attrs["readonly"] = True


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = [
            "amount",
            "phone",
        ]
