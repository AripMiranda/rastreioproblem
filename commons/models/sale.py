import random
import string

from django.db import models

from commons.models.profile import Profile
from commons.models.shop import Shop


class Sale(models.Model):
    """
    Represents a sale associated with a specific shop.

    Attributes:
        - shop: Reference to the shop where the sale occurred.
        - description: A textual description of the sale.
        - value: The monetary value of the sale.
        - sale_date: The date and time when the sale was made.
        - code: A unique code associated with the sale.
        - finished: Indicates if the sale has been completed.
    """
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(default='', blank=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=64, unique=True, editable=False)
    finished = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.

        If the sale does not have a code, it will generate one
        before saving the sale instance.
        """
        if not self.code:
            self.code = self.make_code()
        super(Sale, self).save(*args, **kwargs)

    def make_code(self):
        """
        Generates a unique code for the sale.

        The format of the code is: AAxxxxxxxxxB, where:
        - AA is a prefix of two random uppercase letters.
        - xxxxxxxxx is a series of nine random digits.
        - B is a suffix of two random uppercase letters.

        Returns:
            str: The generated code.
        """
        prefix = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        suffix = ''.join(random.choice(string.ascii_uppercase) for _ in range(2))
        code = ''.join(random.choice(string.digits) for _ in range(9))
        return f"{prefix}{code}{suffix}"

    def __str__(self):
        """
        String representation of the sale instance.

        Returns:
           str: The name of the shop followed by the sale description.
        """
        return f"{self.shop.name} ({self.description})"

    class Meta:
        """Metadata for the Sale model."""
        ordering = ('-sale_date',)
        verbose_name = 'Venda'
