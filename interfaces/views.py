from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
from controle_estoque.models import Produto
from controle_vendas.models import Venda
from controle_pedidos.models import PedidoCompra
import datetime


@login_required()
def homepage(request):
    return render(request, 'homepage.html')


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def dashboard(request):
    """
    Cards Front
    """
    qtd_produtos = Produto.objects.filter(ativo=True).count()
    qtd_produtos_limite_alerta_min = Produto.objects.filter(ativo=True, limite_alerta_min=False).count()
    qtd_vendas = Venda.objects.filter(ativo=True).count()
    qtd_comprados = PedidoCompra.objects.filter(status__in=[1, 2, 3]).count()

    context = {
        'active': 'dashboard',
        'qtd_produtos': qtd_produtos,
        'qtd_vendas': qtd_vendas,
        'qtd_produtos_limite_alerta_min': qtd_produtos_limite_alerta_min,
        'qtd_comprados': qtd_comprados,
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
    return render(request, 'dashboard.html', context)


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def pag_login(request):
    context = {}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                dj_login(request, user)
                return redirect(reverse('homepage'))
        else:
            messages.error(request, "Nome de usuário ou senha incorreta")
            return redirect('login')
    return render(request, 'login.html', context)
