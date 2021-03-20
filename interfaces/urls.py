from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas, lista_pedidos, detalhe_produto, detalhe_pedido, lista_produtos, user_logout

urlpatterns = [
    path('', homepage, name="homepage"),
    path('logout/', user_logout, name="logout"),
    path('app-vendas', appvendas, name="appvendas"),

    # Listagem
    path('lista-pedidos/', lista_pedidos, name="lista-pedidos"),
    path('lista-produtos/', lista_produtos, name="lista-produtos"),

    # Detalhes por object
    path('detalhe-produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
    path('detalhe-pedido/<int:pk>', detalhe_pedido, name='detalhe_pedido'),
]
