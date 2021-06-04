from django import forms
from controle_estoque.models import Produto


class ProdutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['preco_compra'] = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01,
                                                         label="Preço de Compra")
        self.fields['preco_venda'] = forms.DecimalField(max_digits=6, decimal_places=2, min_value=0.01,
                                                        label="Preço de Venda")
        self.fields['total_pecas'] = forms.IntegerField(min_value=0, label="Total de Peças")
        self.fields['min_pecas'] = forms.IntegerField(min_value=0, label="Mín. de Peças")
        self.fields['genero'] = forms.IntegerField(min_value=0, label="Gênero")
        self.fields['descricao'] = forms.IntegerField(min_value=0, label="Descrição")
        self.fields['motivo_alteracao_preco'] = forms.IntegerField(min_value=0, label="Motivo Alteração de Preço")
        self.fields['alerta_min'] = forms.IntegerField(min_value=0, label="Alerta Mín.")

    class Meta:
        model = Produto
        fields = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas', 'alerta_min',
                  'total_pecas', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'fornecedor', 'auto_pedido']
