from django.contrib import admin

from investments.models import (
    InvestCategory,
    PaymentMethod,
    Deposit,
    Withdrawal,
    Package,
    PackagePayment,
    PackageWallet,
)

admin.site.register(InvestCategory)
admin.site.register(PaymentMethod)
admin.site.register(PackagePayment)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Package)
admin.site.register(PackageWallet)
