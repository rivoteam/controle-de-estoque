from django.urls import path
from .views import appvendas, lista_vendas, detalhe_venda

urlpatterns = [
    path('app-vendas/', appvendas, name="appvendas"),
    path('lista-vendas/', lista_vendas, name="lista-vendas"),
    path('detalhe-venda/<int:pk>', detalhe_venda, name='detalhe_venda'),
]
