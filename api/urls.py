from django.urls import path, include
from rest_framework import routers
from .views import ProdutoViewSet, PedidoViewSet, CarrinhoPedidoViewSet, VendaViewSet, CarrinhoVendaViewSet, \
    get_detail_produtos, api_home, ProdutoListApi, post_realiza_vendas, post_realiza_compras

router = routers.DefaultRouter()
router.register('produto', ProdutoViewSet)
router.register('pedido', PedidoViewSet)
router.register('carrinho-pedido', CarrinhoPedidoViewSet)
router.register('venda', VendaViewSet)
router.register('carrinho-venda', CarrinhoVendaViewSet)

urlpatterns = [
    path('drf/', include(router.urls)),
    path('', api_home, name='api_http'),
    path('produtos/', ProdutoListApi.as_view(), name='produto'),
    path('produto/<str:pk>', get_detail_produtos, name='get_produto'),
    path('produto/realiza_vendas/', post_realiza_vendas, name='post_realiza_vendas'),
    path('produto/realiza_compras/', post_realiza_compras, name='post_realiza_compras'),
    path('produto/', get_detail_produtos, name='get_produto'),
    path('api-auth/', include('rest_framework.urls'))

]
