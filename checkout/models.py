import base64
from django.db import models
from accounts.abstracts import UniversalIdModel, TimeStampedModel
from django.db.models.signals import pre_save
from django.dispatch import receiver

from forexapp.settings import SHORTCODE, TRANSACTION_TYPE, CALLBACK_URL, PASS_KEY


class TrialCheckout(UniversalIdModel, TimeStampedModel):
    business_shortcode = models.PositiveBigIntegerField()
    password = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=1000)
    amount = models.PositiveBigIntegerField()
    party_a = models.PositiveBigIntegerField()
    party_b = models.PositiveBigIntegerField()
    phone_number = models.PositiveBigIntegerField()
    callback_url = models.URLField()
    account_reference = models.CharField(max_length=1000)
    transaction_description = models.CharField(max_length=1000)


@receiver(pre_save, sender=TrialCheckout)
def business_shortcode_presave(sender, instance, **kwargs):
    instance.business_shortcode = SHORTCODE


@receiver(pre_save, sender=TrialCheckout)
def password_presave(sender, instance, **kwargs):
    shortcode = str(SHORTCODE)
    passkey = str(PASS_KEY)

    concatenated = f"{shortcode}{passkey}{instance.timestamp}".encode()
    instance.password = base64.b64encode(concatenated).decode()


@receiver(pre_save, sender=TrialCheckout)
def transaction_type_presave(sender, instance, **kwargs):
    instance.transaction_type = TRANSACTION_TYPE


@receiver(pre_save, sender=TrialCheckout)
def party_a_presave(sender, instance, **kwargs):
    instance.party_a = instance.phone_number


@receiver(pre_save, sender=TrialCheckout)
def party_b_presave(sender, instance, **kwargs):
    instance.party_b = SHORTCODE


@receiver(pre_save, sender=TrialCheckout)
def callback_url_presave(sender, instance, **kwargs):
    instance.callback_url = CALLBACK_URL


@receiver(pre_save, sender=TrialCheckout)
def account_reference_presave(sender, instance, **kwargs):
    instance.account_reference = "Test"


@receiver(pre_save, sender=TrialCheckout)
def transaction_description_presave(sender, instance, **kwargs):
    instance.transaction_description = "Test"
