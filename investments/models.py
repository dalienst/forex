from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import UniversalIdModel, TimeStampedModel

User = get_user_model()


class InvestCategory(UniversalIdModel, TimeStampedModel):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, default="Category")
    description = models.TextField()
    price = models.PositiveIntegerField(blank=True, null=True)
    max_price = models.PositiveIntegerField(blank=True, null=True)
    usdt_price = models.FloatField(blank=True, null=True)
    usdt_max = models.FloatField(blank=True, null=True)
    profit_rate = models.CharField(max_length=255, blank=True, null=True)
    daily_withdrawal = models.CharField(max_length=255, blank=True, null=True)
    daily_usdt = models.FloatField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Investment Category"
        verbose_name_plural = "Investment Categories"

    def __str__(self) -> str:
        return self.name


class PaymentMethod(UniversalIdModel, TimeStampedModel):
    """
    Methods of payment
    """

    name = models.CharField(max_length=255)
    detail = models.CharField(max_length=255, blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    wallet = models.CharField(max_length=1000, blank=True, null=True)
    till_number = models.PositiveIntegerField(blank=True, null=True)
    paybill = models.PositiveIntegerField(blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self) -> str:
        return self.name


class Package(UniversalIdModel, TimeStampedModel):
    """
    User selected package
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(InvestCategory, on_delete=models.CASCADE)

    # @property
    # def available_funds(self):
    #     total_deposits = (
    #         self.deposits.aggregate(total=models.Sum("amount"))["total"] or 0
    #     )
    #     total_withdrawals = (
    #         self.withdrawals.aggregate(total=models.Sum("amount"))["total"] or 0
    #     )
    #     return total_deposits - total_withdrawals

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"

    def __str__(self):
        return self.category.name


class Deposit(UniversalIdModel, TimeStampedModel):
    """
    To handle deposit of funds via Mpesa only
    """

    amount = models.PositiveIntegerField()
    phone = models.BigIntegerField()
    trans_ref = models.CharField(max_length=100, unique=True)


class Withdrawal(UniversalIdModel, TimeStampedModel):
    """
    To handle withdrawal of funds via Mpesa only
    """

    amount = models.PositiveIntegerField()
    phone = models.BigIntegerField()
    is_processed = models.BooleanField(default=False)


# class Transaction(UniversalIdModel, TimeStampedModel):
#     package = models.ForeignKey(
#         Package, on_delete=models.CASCADE, related_name="transactions"
#     )
#     amount = models.PositiveIntegerField()
#     transaction_type = models.CharField(
#         max_length=10, choices=[("deposit", "Deposit"), ("withdrawal", "Withdrawal")]
#     )
#     phone = models.BigIntegerField()

#     class Meta:
#         ordering = ["-created_at"]
