import hashlib
import uuid
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone


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
    url_site = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='shop_imgs/', blank=True, null=True)
    premium_expiration_date = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=128, default="")

    @staticmethod
    def authenticate(request, email=email, password=password):
        try:
            shop = Shop.objects.get(email=email)

            if shop.check_password(password):
                return shop
            else:
                return None
        except Shop.DoesNotExist:
            return None

    def set_password(self, password):
        """
        Define a senha da loja após o hashing.
        """
        self.password = make_password(password)

    def check_password(self, password):
        """
        Verifica se a senha fornecida corresponde à senha armazenada.
        """
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        """
        Overrides the default save method.

        If the shop does not have a referral code, it checks for a
        custom referral code. If none exists, it generates a new
        referral code before saving the shop instance.
        """
        if not self.pk:  # Check if this is a new shop instance
            self.premium_expiration_date = timezone.now() + timedelta(days=7)

        if not self.referral:
            self.referral = self.make_referral()
        elif self.custom_referral:
            self.referral = self.custom_referral
        if self.password:
            if not self.id or (self.id and self.password != self._get_password()):
                self.set_password(self.password)

        super(Shop, self).save(*args, **kwargs)

    def _get_password(self):
        """
        Retrieve the password from the database for comparison.
        """
        if self.id:
            return Shop.objects.values_list('password', flat=True).get(id=self.id)
        return None

    def has_sufficient_balance(self, cpf_count, cost_per_cpf):
        """
        Verifica se a loja tem saldo suficiente para processar os CPFs.

        Args:
        - cpf_count: O número de CPFs a serem processados.
        - cost_per_cpf: O custo em pontos para processar um CPF.

        Returns:
        - bool: True se tiver saldo suficiente, False caso contrário.
        """
        return self.points_balance >= cpf_count * cost_per_cpf

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
