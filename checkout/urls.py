# urls.py
from django.urls import path
from checkout.views import trial_checkout_view

app_name = "checkout"

urlpatterns = [
    path("pay/", trial_checkout_view, name="make-payment"),
    # Add other URLs as needed
]
