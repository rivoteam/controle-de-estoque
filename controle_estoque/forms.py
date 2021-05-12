from django import forms

from controle_estoque.models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas', 'alerta_min',
                  'total_pecas', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'fornecedor', 'auto_pedido']
