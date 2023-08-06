from django.db import models

from commons.models.sale import Sale


class Tracking(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_tracking')
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return f"{self.description} em {self.updated_at.strftime('%d/%m/%Y %H:%M')}"
