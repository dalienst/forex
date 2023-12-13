import requests
import base64
from django.shortcuts import render
from django.utils import timezone
from checkout.forms import TrialCheckoutForm

from forexapp.settings import (
    SHORTCODE,
    TRANSACTION_TYPE,
    CALLBACK_URL,
    PASS_KEY,
    CONSUMER_KEY,
    CONSUMER_SECRET,
)


def trial_checkout_view(request):
    if request.method == "POST":
        form = TrialCheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data
            amount = form.cleaned_data["amount"]
            phone_number = form.cleaned_data["phone_number"]

            # Get access token
            access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
            auth_response = requests.get(
                access_token_url, auth=(CONSUMER_KEY, CONSUMER_SECRET)
            )
            auth_data = auth_response.json()
            access_token = auth_data.get("access_token")

            if not access_token:
                return render(
                    request,
                    "payment_form.html",
                    {"form": form, "error": "Unable to obtain access token"},
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

            payload = {
                "BusinessShortCode": SHORTCODE,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": TRANSACTION_TYPE,
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": SHORTCODE,
                "PhoneNumber": phone_number,
                "CallBackURL": CALLBACK_URL,
                "AccountReference": "Test",
                "TransactionDesc": "Test",
            }

            # Make the API call
            api_response = requests.post(api_url, json=payload, headers=headers)
            response_data = api_response.json()

            return render(
                request,
                "success_template.html",
                {"message": response_data, "form": form},
            )
    else:
        form = TrialCheckoutForm()

    return render(request, "payment_form.html", {"form": form})
