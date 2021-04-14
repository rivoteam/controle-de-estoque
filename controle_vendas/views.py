from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from controle_estoque.models import Produto
from .models import Venda
from .forms import VendaForm


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_cashier(), login_url="/", redirect_field_name=None)
def appvendas(request):
    context = {
        'form': VendaForm(),
        'produtos': Produto.objects.all(),
        "active": "app-vendas"
    }
    return render(request, 'app_venda.html', context)


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst_or_cashier_or_seller(), login_url="/", redirect_field_name=None)
def lista_vendas(request):
    context = {
        "vendas": Venda.objects.filter(ativo=True),
        "active": "lista-vendas"
    }
    return render(request, 'vendas.html', context)


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst_or_cashier_or_seller(), login_url="/", redirect_field_name=None)
def detalhe_venda(request, pk):
    venda = Venda.objects.get(pk=pk)
    produtos = venda.carrinhovenda_set.all()
    context = {
        'venda': venda,
        'produtos': produtos,
    }
    return render(request, 'modal_detalhe_venda.html', context)
