from django.db.models.signals import post_save
from django.dispatch import receiver
from investments.models import Deposit, Withdrawal, Transaction


@receiver(post_save, sender=Deposit)
@receiver(post_save, sender=Withdrawal)
def create_transaction(sender, instance, created, **kwargs):
    if created:
        # Determine the transaction type based on the sender model
        transaction_type = "deposit" if isinstance(instance, Deposit) else "withdrawal"

        # Create a Transaction instance
        Transaction.objects.create(
            package=instance.package,
            amount=instance.amount,
            transaction_type=transaction_type,
            phone=instance.phone,
        )
