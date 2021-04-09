from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra
from controle_vendas.models import Venda
import datetime
from controle_vendas.forms import VendaForm


@login_required()
def homepage(request):
    """
    Cards Front
    """
    qtd_produtos = Produto.objects.filter(ativo=True).count()
    qtd_produtos_limite_alerta_min = Produto.objects.filter(ativo=True, limite_alerta_min=False).count()
    qtd_vendas = Venda.objects.filter(ativo=True).count()

    context = {
        'active': 'homepage',
        'qtd_produtos': qtd_produtos,
        'qtd_vendas': qtd_vendas,
        'qtd_produtos_limite_alerta_min': qtd_produtos_limite_alerta_min
    }

    """
    Vendas por mes
    """
    today = datetime.datetime.today()
    first_day_in_month = today.replace(day=1)
    for i in range(12):
        vendido_no_mes = 0
        mes = first_day_in_month.strftime("%Y-%m")
        vendas = Venda.objects.filter(criado_em__startswith=mes)
        context[f'mes_{i}'] = mes
        for venda in vendas:
            vendido_no_mes += int(venda.calc_faturamento())
        context[f'registro_{i}'] = vendido_no_mes
        last_month = first_day_in_month - datetime.timedelta(days=1)
        first_day_in_month = last_month.replace(day=1)
    return render(request, 'homepage.html', context)


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def appvendas(request):
    context = {
        'form': VendaForm(),
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
    pedido = PedidoCompra.objects.get(pk=pk)
    produtos = pedido.carrinhopedido_set.all()
    context = {
        'pedido': pedido,
        'produtos': produtos,
    }
    return render(request, 'modal_detalhe_pedido.html', context)
