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
        ]


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
