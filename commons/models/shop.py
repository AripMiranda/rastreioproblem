import hashlib
import uuid

from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    referral = models.CharField(max_length=64, unique=True, editable=False)
    custom_referral = models.CharField(max_length=64, blank=True, default='')
    points_balance = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.referral:
            if self.custom_referral:
                self.referral = self.custom_referral
            else:
                self.referral = self.make_referral()
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def make_referral(self):
        hash_base = f"{self.id}-{uuid.uuid4()}"
        return hashlib.sha256(hash_base.encode()).hexdigest()
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Loja'
