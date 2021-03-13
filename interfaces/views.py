from django.shortcuts import render
from core.settings import STATIC_URL
from controle_estoque.models import Produto
from core.utils import get_user_profile
from controle_pedidos.models import PedidoCompra

def homepage(request):
    context_user = get_user_profile(request)
    context = {}
    context.update(context_user)
    return render(request, 'homepage.html', context)


def appvendas(request):
    context = {
        'produtos': Produto.objects.all()
    }
    context_user = get_user_profile(request)
    context.update(context_user)
    return render(request, 'app-venda.html', context)


def lista_pedidos(request):
    context_user = get_user_profile(request)
    context = {
        "pedidos": PedidoCompra.objects.all()
    }
    context.update(context_user)
    return render(request, 'pedidos.html', context)
