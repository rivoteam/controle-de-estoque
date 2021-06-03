from django import forms
from controle_estoque.models import Produto


class ProdutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco_compra'] = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01)
        self.fields['preco_venda'] = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01)
        self.fields['total_pecas'] = forms.IntegerField(min_value=1)

    class Meta:
        model = Produto
        fields = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas', 'alerta_min',
                  'total_pecas', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'fornecedor', 'auto_pedido']
