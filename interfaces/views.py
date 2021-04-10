from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from controle_estoque.models import Produto
from controle_vendas.models import Venda
from interfaces.forms import ProdutoForm
import datetime


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

