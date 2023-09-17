from django import forms

from commons.models.shop import Shop


class ShopForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Shop
        fields = ['name', 'email', 'password']

    def clean_email(self):
        """
        Validação personalizada para garantir que o e-mail seja único.
        """
        email = self.cleaned_data['email']
        if Shop.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
