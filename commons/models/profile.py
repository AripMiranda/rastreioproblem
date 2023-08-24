from django.db import models


class Profile(models.Model):
    """
    Represents a user's profile with additional information such as name, CPF, and RG.

    Attributes:
        - name: The name of the user.
        - cpf: The user's CPF (Cadastro de Pessoas Físicas) number.

    """
    name = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, unique=True)

    class Meta:
        """Metadata for the Profile model."""
        ordering = ('-id',)
        verbose_name = 'Usuário'

    def __str__(self):
        """
        String representation of the user profile instance.

        Returns:
            str: The name of the user.
        """
        return self.cpf
