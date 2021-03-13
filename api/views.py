from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra, CarrinhoPedido
from controle_vendas.models import Venda, CarrinhoVenda
from .serializers import ProdutoSerializer, PedidoSerializer, CarrinhoPedidoSerializer, VendaSerializer, \
    CarrinhoVendaSerializer


class ProdutoViewSet(ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

# class ProdutoViewSet(viewsets.ModelViewSet):
#     queryset = Produto.objects.all()
#     serializer_class = ProdutoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoSerializer


class CarrinhoPedidoViewSet(viewsets.ModelViewSet):
    queryset = CarrinhoPedido.objects.all()
    serializer_class = CarrinhoPedidoSerializer


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer


class CarrinhoVendaViewSet(viewsets.ModelViewSet):
    queryset = CarrinhoVenda.objects.all()
    serializer_class = CarrinhoVendaSerializer
