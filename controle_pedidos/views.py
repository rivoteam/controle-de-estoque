from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from controle_pedidos.models import PedidoCompra, CarrinhoPedido
from controle_pedidos.forms import PedidoForm
from controle_estoque.models import Produto, Fornecedor
from django.conf import settings
from django.core.mail import send_mail


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst_or_stockist(), login_url="/", redirect_field_name=None)
def lista_pedidos(request):
    context = {
        "pedidos": PedidoCompra.objects.filter(ativo=True),
        "active": "lista-pedidos"
    }
    return render(request, 'lista_pedidos.html', context)


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst_or_stockist(), login_url="/", redirect_field_name=None)
def detalhe_pedido(request, pk):
    pedido = PedidoCompra.objects.get(pk=pk)
    produtos = pedido.carrinhopedido_set.all()
    context = {
        'pedido': pedido,
        'produtos': produtos,
    }
    return render(request, 'modal_detalhe_pedido.html', context)


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_cria_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        form.instance.criado_por = request.user
        form.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_cria_pedido.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_atualiza_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    form = PedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        pedido.atualizado_por = request.user
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_atualiza_pedido.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_remove_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    if request.POST:
        pedido.atualizado_por = request.user
        pedido.ativo = False
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    else:
        return render(request, 'modal_remove_pedido.html', {'pedido': pedido})


def envia_email(fornecedor_email, fornecedor, produtos):
    mensagem = f"Compra de {len(produtos)} produtos, de acordo com o seguinte:\n{produtos}"
    subject = f"Compra de produtos - {fornecedor}"
    mail = send_mail(
        subject=subject, message=mensagem, recipient_list=fornecedor_email, from_email=settings.EMAIL_BACKEND
    )
    return mail


def compra_automatica_produtos():
    """
    Realiza compra automática de produtos em alerta minimo
    """
    produtos_em_alerta = Produto.objects.filter(ativo=True, limite_alerta_min=True)
    temp_list = []
    for produto in produtos_em_alerta:
        temp_list.append(produto.fornecedor)
    fornecedores_instance = set(temp_list)

    for fornecedor in fornecedores_instance:
        pedido = PedidoCompra.objects.create(fornecedor=fornecedor, criado_por=User.objects.first(),
                                             atualizado_por=User.objects.first())
        compra = {}
        valor_compra = 0
        i = 1
        for produto in produtos_em_alerta:
            if produto.fornecedor == fornecedor:
                valor_compra += ((produto.min_pecas - produto.total_pecas) * produto.preco_compra)
                compra[i] = {
                    "produto": produto.ean,
                    "tamanho": produto.tamanho,
                    "quantidade": (produto.min_pecas - produto.total_pecas)
                }
                if valor_compra >= fornecedor.faturamento_minimo:
                    CarrinhoPedido.objects.create(quantidade=(produto.min_pecas - produto.total_pecas), produto=produto,
                                                  pedidocompra=pedido)
                    i += 1
                else:
                    pedido.delete()
                    return
        envia_email(fornecedor_email=fornecedor.email, fornecedor=fornecedor.nome_empresa, produtos=compra)


def app_compra(request):
    context = {
        'form': PedidoForm(),
        'produtos': Produto.objects.all(),
        "active": "app_compra"
    }
    return render(request, 'app_compra.html', context)
