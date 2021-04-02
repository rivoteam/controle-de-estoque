from django import forms

from controle_estoque.models import Produto


class NovoProdutoForm(forms.ModelForm):
        class Meta:
            model = Produto
            fields = "__all__"