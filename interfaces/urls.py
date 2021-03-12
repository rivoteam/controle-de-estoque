from django.contrib import admin
from django.urls import path
from .views import homepage, detalhe_produto

urlpatterns = [
    path('', homepage, name="homepage"),
    path('detalhe/produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
]
