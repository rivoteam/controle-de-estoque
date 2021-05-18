from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra, CarrinhoPedido
from controle_vendas.models import Venda, CarrinhoVenda
from rest_framework import serializers


class ProdutoSerializer(serializers.ModelSerializer):
    nome_categoria = serializers.CharField(source='categoria')
    nome_subcategoria = serializers.CharField(source='subcategoria')
    nome_fornecedor = serializers.CharField(source='fornecedor')

    class Meta:
        model = Produto
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoCompra
        fields = '__all__'


class CarrinhoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrinhoPedido
        fields = '__all__'


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class CarrinhoVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrinhoVenda
        fields = '__all__'
