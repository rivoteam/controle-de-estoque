from django.urls import path, include
from rest_framework import routers
from .views import ProdutoViewSet, PedidoViewSet, CarrinhoPedidoViewSet, VendaViewSet, CarrinhoVendaViewSet

router = routers.DefaultRouter()
# router.register('produto', ProdutoViewSet)
router.register('pedido', PedidoViewSet)
router.register('carrinho-pedido', CarrinhoPedidoViewSet)
router.register('venda', VendaViewSet)
router.register('carrinho-venda', CarrinhoVendaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('prod/', ProdutoViewSet.as_view({'get': 'list'}), name='prod'),
    path('prod/', ProdutoViewSet.as_view(), name='prod'),
    path('api-auth/', include('rest_framework.urls'))

]
