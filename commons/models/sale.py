import random
import string

from django.db import models

from commons.models.shop import Shop


class Sale(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=64, unique=True, editable=False)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.make_code()
        super(Sale, self).save(*args, **kwargs)

    def make_code(self):
        prefix = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        suffix = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        code = ''.join(random.choice(string.digits) for _ in range(9))
        return f"{prefix}{code}{suffix}"

    def __str__(self):
        return f"{self.shop.name} ({self.description})"
    
    class Meta:
        ordering = ('-sale_date',)
        verbose_name = 'Venda'
