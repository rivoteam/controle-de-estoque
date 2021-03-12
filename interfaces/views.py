from django.shortcuts import render

from controle_estoque.models import Produto
from core.settings import STATIC_URL
from controle_estoque.models import Produto
from core.utils import get_user_profile


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


def detalhe_produto(request, pk):
    context = {
        'produto': Produto.objects.get(pk=pk)
    }
    return render(request, 'produto_detalhe.html', context)
