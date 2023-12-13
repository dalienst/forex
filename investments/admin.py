from django.contrib import admin

from investments.models import (
    InvestCategory,
    PaymentMethod,
    Transaction,
    Deposit,
    Withdrawal,
    Package,
)

admin.site.register(InvestCategory)
admin.site.register(PaymentMethod)
admin.site.register(Transaction)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Package)
