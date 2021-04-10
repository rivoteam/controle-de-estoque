from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from controle_pedidos.models import PedidoCompra
from controle_pedidos.forms import PedidoForm


@login_required()
def lista_pedidos(request):
    context = {
        "pedidos": PedidoCompra.objects.filter(ativo=True),
        "active": "lista-pedidos"
    }
    return render(request, 'lista_pedidos.html', context)


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
def modal_cria_pedido(request):
    form = PedidoForm(request.POST or None)
    if form.is_valid():
        form.instance.criado_por = request.user
        form.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_cria_pedido.html', {'form': form})


@login_required()
def modal_atualiza_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    form = PedidoForm(request.POST or None, instance=pedido)
    if form.is_valid():
        pedido.atualizado_por = request.user
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    return render(request, 'modal_atualiza_pedido.html', {'form': form})


@login_required()
def modal_remove_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    if request.POST:
        pedido.atualizado_por = request.user
        pedido.ativo = False
        pedido.save()
        return redirect(reverse('lista-pedidos'))
    else:
        return render(request, 'modal_remove_pedido.html', {'pedido': pedido})
