# forms.py
from django import forms


class TrialCheckoutForm(forms.Form):
    amount = forms.IntegerField()
    phone_number = forms.IntegerField()
    # Add other fields as needed

