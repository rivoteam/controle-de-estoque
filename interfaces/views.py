from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView

from controle_estoque.models import Produto
from controle_pedidos.models import PedidoCompra
from controle_vendas.models import Venda


@login_required()
def homepage(request):
    return render(request, 'homepage.html', {'active': 'homepage'})

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
        "vendas": Venda.objects.all(),
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


class ModalCriaPedido(CreateView):
    template_name = "modal_cria_pedido.html"
    model = PedidoCompra
    fields = "__all__"
    context_object_name = "form"
    success_url = reverse_lazy("lista-pedidos")

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class ModalAtualizaPedido(UpdateView):
    template_name = "modal_atualiza_pedido.html"
    model = PedidoCompra
    fields = "__all__"
    context_object_name = "form"
    success_url = reverse_lazy("lista-pedidos")

    def form_valid(self, form):
        form.instance.atualizado_por = self.request.user
        return super().form_valid(form)


@login_required()
def modal_remove_pedido(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    context = {
        'pedido': pedido,
    }
    return render(request, 'modal_remove_pedido.html', context)


@login_required()
def remove_pedido(request, pk):
    pedido = PedidoCompra.objects.get(pk=pk)
    pedido.delete()
    return redirect(reverse('lista-pedidos'))


modal_atualiza_pedido = ModalAtualizaPedido.as_view()
modal_cria_pedido = ModalCriaPedido.as_view()
