from django import forms
from .models import Venda


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['forma_pagto', 'vendedor']
        widgets = {
            'forma_pagto': forms.Select(attrs={
                'class': 'form-control',
                'id': 'pagamento',
            }),
            'vendedor': forms.Select(attrs={
                'class': 'form-control',
                'id': 'vendedor',
            })
        }
