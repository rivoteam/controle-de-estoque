from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra


@login_required()
def homepage(request):
    return render(request, 'homepage.html')

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def appvendas(request):
    context = {
        'produtos': Produto.objects.all(),
        "active": "app-vendas"
    }
    return render(request, 'app_venda.html', context)


@login_required()
def lista_produtos(request):
    context = {
        "produtos": Produto.objects.all(),
        "active": "lista-produtos"
    }
    return render(request, 'produtos.html', context)

@login_required()
def detalhe_produto(request, pk):
    context = {
        'produto': Produto.objects.get(pk=pk),
    }
    return render(request, 'modal_detalhe_produto.html', context)


@login_required()
def lista_pedidos(request):
    context = {
        "pedidos": PedidoCompra.objects.all(),
        "active": "lista-pedidos"
    }
    return render(request, 'pedidos.html', context)


@login_required()
def detalhe_pedido(request, pk):
    context = {
        'produto': PedidoCompra.objects.get(pk=pk),
    }
    return render(request, 'modal_detalhe_pedido.html', context)
