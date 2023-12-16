from django import forms

from investments.models import (
    InvestCategory,
    Deposit,
    Withdrawal,
    Package,
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
            "payment_method",
        ]


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = [
            "package",
            "amount",
            "phone",
        ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["package"].queryset = Package.objects.filter(user=user)


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = [
            "package",
            "amount",
            "phone",
        ]
