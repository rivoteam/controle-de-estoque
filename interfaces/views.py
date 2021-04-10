from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra
from controle_vendas.models import Venda
import datetime
from controle_vendas.forms import VendaForm
from interfaces.forms import PedidoForm, ProdutoForm


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
        "produtos": Produto.objects.filter(ativo=True),
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
        "pedidos": PedidoCompra.objects.filter(ativo=True),
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


@login_required()
def lista_vendas(request):
    context = {
        "vendas": Venda.objects.filter(ativo=True),
        "active": "lista-vendas"
    }
    return render(request, 'vendas.html', context)


@login_required()
def detalhe_venda(request, pk):
    venda = Venda.objects.get(pk=pk)
    produtos = venda.carrinhovenda_set.all()
    context = {
        'venda': venda,
        'produtos': produtos,
    }
    return render(request, 'modal_detalhe_venda.html', context)


@login_required()
def modal_cria_produto(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.instance.criado_por = request.user
        form.save()
        return redirect(reverse('lista-produtos'))
    return render(request, 'modal_cria_produto.html', {'form': form})


def modal_atualiza_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        produto.atualizado_por = request.user
        produto.save()
        return redirect(reverse('lista-produtos'))
    return render(request, 'modal_atualiza_produto.html', {'form': form})


def modal_remove_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.POST:
        produto.atualizado_por = request.user
        produto.ativo = False
        produto.save()
        return redirect(reverse('lista-produtos'))
    else:
        return render(request, 'modal_remove_produto.html', {'produto': produto})

@login_required()
def modal_cria_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        form.instance.criado_por = request.user
        form.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_cria_pedido.html', {'form': form})


def modal_atualiza_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    form = PedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        pedido.atualizado_por = request.user
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_atualiza_pedido.html', {'form': form})


def modal_remove_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    if request.POST:
        pedido.atualizado_por = request.user
        pedido.ativo = False
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    else:
        return render(request, 'modal_remove_pedido.html', {'pedido': pedido})
