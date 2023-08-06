from celery import shared_task

from commons.models.sale import Sale

from datetime import timedelta
from django.utils import timezone

from commons.models.tracking import Tracking


@shared_task
def update_sales():
    threshold_date = timezone.now() - timedelta(days=3)

    sales_to_update = Sale.objects.filter(done=False).exclude(sale_tracking__update__gte=threshold_date)

    for sale in sales_to_update:
        next_step(sale)


def next_step(sale):
    description = "Sua descrição aqui"

    Tracking.objects.create(sale=sale, description=description)
