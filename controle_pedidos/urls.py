from django.urls import path
from .views import app_compra, lista_pedidos, detalhe_pedido, modal_cria_pedido, modal_atualiza_pedido, \
    modal_remove_pedido, finaliza_pedido

urlpatterns = [
    path('app-compra/', app_compra, name="app_compra"),
    path('lista-pedidos/', lista_pedidos, name="lista-pedidos"),
    path('detalhe-pedido/<int:pk>', detalhe_pedido, name='detalhe_pedido'),
    path('finaliza-pedido/<int:pk>', finaliza_pedido, name='finaliza_pedido'),
    path('modal-cria-pedido/', modal_cria_pedido, name='modal-cria-pedido'),
    path('modal-atualiza-pedido/<int:pk>', modal_atualiza_pedido, name='modal-atualiza-pedido'),
    path('modal-remove-pedido/<int:pk>', modal_remove_pedido, name='modal-remove-pedido'),
]
