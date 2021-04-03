from django import forms

from controle_pedidos.models import PedidoCompra


class PedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoCompra
        fields = "__all__"
