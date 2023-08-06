from django import forms

from commons.models.sale import Sale


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['description', 'value']
