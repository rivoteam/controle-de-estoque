from django.urls import path
from .views import lista_pedidos, detalhe_pedido, modal_cria_pedido, modal_atualiza_pedido, modal_remove_pedido

urlpatterns = [
    path('lista-pedidos/', lista_pedidos, name="lista-pedidos"),
    path('detalhe-pedido/<int:pk>', detalhe_pedido, name='detalhe_pedido'),
    path('modal-cria-pedido/', modal_cria_pedido, name='modal-cria-pedido'),
    path('modal-atualiza-pedido/<int:pk>', modal_atualiza_pedido, name='modal-atualiza-pedido'),
    path('modal-remove-pedido/<int:pk>', modal_remove_pedido, name='modal-remove-pedido'),
]
