from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas, lista_pedidos, detalhe_produto, detalhe_pedido, lista_produtos, user_logout, \
    lista_vendas, detalhe_venda, modal_cria_pedido, modal_atualiza_pedido, modal_remove_pedido, remove_pedido

urlpatterns = [
    path('', homepage, name="homepage"),
    path('logout/', user_logout, name="logout"),
    path('app-vendas', appvendas, name="appvendas"),

    # Listagem
    path('lista-pedidos', lista_pedidos, name="lista-pedidos"),
    path('lista-produtos', lista_produtos, name="lista-produtos"),
    path('lista-vendas', lista_vendas, name="lista-vendas"),

    # Detalhes por object
    path('detalhe-produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
    path('detalhe-pedido/<int:pk>', detalhe_pedido, name='detalhe_pedido'),
    path('detalhe-venda/<int:pk>', detalhe_venda, name='detalhe_venda'),

    # Criação
    path('modal-cria-pedido', modal_cria_pedido, name='modal-cria-pedido'),

    # Atualização
    path('modal-atualiza-pedido/<int:pk>', modal_atualiza_pedido, name='modal-atualiza-pedido'),

    # Remoção
    path("remove-pedido/<int:pk>", remove_pedido, name="remove-pedido"),
    path('modal-remove-pedido/<int:pk>', modal_remove_pedido, name='modal-remove-pedido'),
]
