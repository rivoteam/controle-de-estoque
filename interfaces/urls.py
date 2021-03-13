from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas, lista_pedidos

urlpatterns = [
    path('', homepage, name="homepage"),
    path('app-vendas', appvendas, name="appvendas"),
    path('lista-pedidos', lista_pedidos, name="lista-pedidos"),
]
