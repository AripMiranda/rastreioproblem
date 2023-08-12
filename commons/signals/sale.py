from django.db.models.signals import post_save
from django.dispatch import receiver

from commons.models.sale import Sale
from commons.models.tracking import Tracking


@receiver(post_save, sender=Sale)
def create_initial_tracking(sender, instance, created, **kwargs):
    """
    Signal handler to create an initial tracking record after a sale instance is saved.

    Whenever a new Sale instance is created and saved to the database, this function
    will be automatically triggered, and it will create an initial tracking record
    with a description indicating that the purchase process has begun.

    Args:
        sender (Model): The model class that sent the signal (in this case, Sale).
        instance (Sale): The actual instance of the sale that was just saved.
        created (bool): Indicates whether this is a new record or an update to an existing record.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Tracking.objects.create(
            sale=instance,
            description="Processando pedido"
        )
