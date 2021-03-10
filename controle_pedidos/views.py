from django.shortcuts import render
from .models import PedidoItem, Pedido, Produto

PedidoItem.objects.create(produto=Produto.objects.last(), quantidade=5)
