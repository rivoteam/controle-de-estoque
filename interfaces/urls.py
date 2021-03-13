from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas, lista_pedidos, detalhe_produto

urlpatterns = [
    path('', homepage, name="homepage"),
    path('app-vendas', appvendas, name="appvendas"),
    path('detalhe/produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
    path('lista-pedidos', lista_pedidos, name="lista-pedidos"),
]
