from django.db.models.signals import post_save
from django.dispatch import receiver

from commons.models.sale import Sale
from commons.models.tracking import Tracking


@receiver(post_save, sender=Sale)
def create_initial_tracking(sender, instance, created, **kwargs):
    if created:
        Tracking.objects.create(
            sale=instance,
            description="Processando compra"
        )
