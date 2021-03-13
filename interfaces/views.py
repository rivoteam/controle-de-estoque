from django.shortcuts import render
from controle_estoque.models import Produto
from core.utils import get_user_profile
from controle_pedidos.models import PedidoCompra


def homepage(request):
    context_user = get_user_profile(request)
    context = {
        "active": "homepage"
    }
    context.update(context_user)
    return render(request, 'homepage.html', context)


def appvendas(request):
    context = {
        'produtos': Produto.objects.all(),
        "active": "app-vendas"
    }
    context_user = get_user_profile(request)
    context.update(context_user)
    return render(request, 'app_venda.html', context)


def detalhe_produto(request, pk):
    context = {
        'produto': Produto.objects.get(pk=pk),
    }
    return render(request, 'detalhe_produto.html', context)


def lista_pedidos(request):
    context_user = get_user_profile(request)
    context = {
        "pedidos": PedidoCompra.objects.all(),
        "active": "lista-pedidos"
    }
    context.update(context_user)
    return render(request, 'pedidos.html', context)


def detalhe_pedido(request, pk):
    context = {
        'produto': PedidoCompra.objects.get(pk=pk),
    }
    return render(request, 'modal_detalhe_pedido.html', context)
