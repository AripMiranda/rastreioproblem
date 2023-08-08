import hashlib
import uuid

from django.db import models


class Shop(models.Model):
    """
    Represents a shop with attributes such as name, email,
    creation date, referral codes, and a balance of points.

    Attributes:
        - name: The name of the shop.
        - email: The email associated with the shop.
        - created_date: The date and time when the shop was created.
        - referral: A unique referral code associated with the shop.
        - custom_referral: A custom referral code that can be set manually.
        - points_balance: The balance of points associated with the shop.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    referral = models.CharField(max_length=64, unique=True, editable=False)
    custom_referral = models.CharField(max_length=64, blank=True, default='')
    points_balance = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.

        If the shop does not have a referral code, it checks for a
        custom referral code. If none exists, it generates a new
        referral code before saving the shop instance.
        """
        if not self.referral:
            if self.custom_referral:
                self.referral = self.custom_referral
            else:
                self.referral = self.make_referral()
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the shop instance.

        Returns:
            str: The name of the shop.
        """
        return self.name

    def make_referral(self):
        """
        Generates a unique referral code for the shop.

        The referral code is a SHA-256 hash derived from a combination
        of the shop's ID and a random UUID.

        Returns:
            str: The generated referral code.
        """
        hash_base = f"{self.id}-{uuid.uuid4()}"
        return hashlib.sha256(hash_base.encode()).hexdigest()

    class Meta:
        """Metadata for the Shop model."""
        ordering = ('-created_date',)
        verbose_name = 'Loja'
