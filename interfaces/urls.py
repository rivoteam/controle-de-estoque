from django.contrib import admin
from django.urls import path
from .views import homepage, detalhe_produto

from .views import homepage, appvendas

urlpatterns = [
    path('', homepage, name="homepage"),
    path('app-vendas', appvendas, name="appvendas"),
    path('detalhe/produto/<int:pk>', detalhe_produto, name='detalhe_produto'),

]
