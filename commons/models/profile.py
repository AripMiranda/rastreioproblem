from django.db import models


class Profile(models.Model):
    """
    Represents a user's profile with additional information such as name, CPF, and RG.

    Attributes:
        - user: A one-to-one relationship to the User model, representing the associated user.
        - name: The name of the user.
        - cpf: The user's CPF (Cadastro de Pessoas Físicas) number.
        - rg: The user's RG (Registro Geral) number.
    """
    name = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=14, unique=True)

    def __str__(self):
        """
        String representation of the user profile instance.

        Returns:
            str: The name of the user.
        """
        return self.cpf
