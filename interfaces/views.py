from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

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


# @login_required()
class CriaProduto(CreateView):
    template_name = "cria-produto.html"
    model = Produto
    fields = "__all__"
    context_object_name = "form"
    success_url = reverse_lazy("lista-produtos")

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

# @login_required()
class AtualizaProduto(UpdateView):
    template_name = "cria-produto.html"
    model = Produto
    fields = "__all__"
    success_url = reverse_lazy("lista-produtos")

    def form_valid(self, form):
        form.instance.atualizado_por = self.request.user
        return super().form_valid(form)

# @login_required()
# def remove_produto(request, pk):
#     produto = Produto.objects.get(pk=pk)
#     produto.delete()
#     return HttpResponseRedirect("/lista-produtos")


cria_produto = CriaProduto.as_view()
atualiza_produto = AtualizaProduto.as_view()


@login_required()
def modal_remove_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    context = {
        'produto': produto,
    }
    return render(request, 'modal_remove_produto.html', context)


@login_required()
def remove_produto(request, pk):
    produto = Produto.objects.get(pk=pk)
    produto.ativo = False
    produto.save()
    return redirect(reverse('lista-produtos'))

