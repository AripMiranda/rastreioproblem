from django.db import models

from commons.models.sale import Sale


class Tracking(models.Model):
    """
    Represents a tracking record associated with a sale.

    Each instance of Tracking corresponds to a specific update or
    event related to a sale. It provides a detailed description
    of the update and a timestamp for when the update occurred.

    Attributes:
        - sale: A foreign key relationship to the Sale model, which
                represents the sale that this tracking record is associated with.
        - description: A detailed description of the tracking update or event.
        - updated_at: The date and time when the tracking update or event occurred.
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_tracking')
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata for the Tracking model."""
        ordering = ['updated_at']
        verbose_name = 'Rastreamento'

    def __str__(self):
        """
        String representation of the tracking instance.

        Returns:
            str: A description of the tracking update, along with the date and time it occurred.
        """
        return f"{self.description} em {self.updated_at.strftime('%d/%m/%Y %H:%M')}"
