from django import forms
from django.core.exceptions import ValidationError
from validate_docbr import CPF

from commons.models.profile import Profile


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cpf', 'email']

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if not CPF().validate(cpf):
            print('cpf cagado')
            raise ValidationError('CPF inválido')
        return cpf
