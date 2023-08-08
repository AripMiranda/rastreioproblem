from celery import shared_task

from commons.models.sale import Sale

from datetime import timedelta
from django.utils import timezone

from commons.models.tracking import Tracking


@shared_task
def update_sales():
    """
    A Celery shared task to update sales which have not been updated within the last 3 days.

    This task looks for Sales which are not done and have not had any tracking
    updates within the last three days. It then calls the next_step function
    for each such sale to add the next tracking step.

    """
    threshold_date = timezone.now() - timedelta(days=3)

    sales_to_update = Sale.objects.filter(done=False).exclude(sale_tracking__update__gte=threshold_date)

    for sale in sales_to_update:
        next_step(sale)


def next_step(sale):
    """
    Adds a new tracking step to the given sale.

    Given a Sale instance, this function creates a new Tracking record
    with a predefined description.

    Args:
        sale (Sale): The sale instance to which a new tracking step will be added.
    """
    description = "Sua descrição aqui"

    Tracking.objects.create(sale=sale, description=description)
