from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas, lista_pedidos, detalhe_produto, detalhe_pedido, lista_produtos, user_logout, \
    lista_vendas, cria_produto, atualiza_produto, remove_produto

urlpatterns = [
    path('', homepage, name="homepage"),
    path('logout/', user_logout, name="logout"),
    path('app-vendas', appvendas, name="appvendas"),

    # Listagem
    path('lista-pedidos', lista_pedidos, name="lista-pedidos"),
    path('lista-produtos', lista_produtos, name="lista-produtos"),
    path('lista-vendas', lista_vendas, name="lista-vendas"),


    # Criação
    path("cria-produto", cria_produto, name="cria-produto"),
    path("atualiza-produto/<int:pk>", atualiza_produto, name="atualiza-produto"),
    path("remove-produto/<int:pk>", remove_produto, name="remove-produto"),


    # Detalhes por object
    path('detalhe-produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
    path('detalhe-pedido/<int:pk>', detalhe_pedido, name='detalhe_pedido'),
]
