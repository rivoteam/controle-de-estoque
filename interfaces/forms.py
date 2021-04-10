from django import forms

from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra


class PedidoForm(forms.ModelForm):
    class Meta:
        model = PedidoCompra
        fields = ['status', 'descricao', 'fornecedor', 'nota_fiscal']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas', 'alerta_min',
                  'total_pecas', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'fornecedor', 'auto_pedido']