from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from controle_estoque.models import Produto
from controle_estoque.forms import ProdutoForm


@login_required()
def lista_produtos(request):
    context = {
        "produtos": Produto.objects.filter(ativo=True),
        "active": "lista-produtos"
    }
    return render(request, 'lista_produtos.html', context)


@login_required()
def detalhe_produto(request, pk):
    context = {
        'produto': Produto.objects.get(pk=pk),
    }
    return render(request, 'modal_detalhe_produto.html', context)


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_cria_produto(request):
    form = ProdutoForm(request.POST or None)
    if form.is_valid():
        form.instance.criado_por = request.user
        form.save()
        return redirect(reverse('lista-produtos'))
    return render(request, 'modal_cria_produto.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_atualiza_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    form = ProdutoForm(request.POST or None, instance=produto)
    if form.is_valid():
        produto.atualizado_por = request.user
        produto.save()
        return redirect(reverse('lista-produtos'))
    return render(request, 'modal_atualiza_produto.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.funcionario.is_manager_or_analyst(), login_url="/", redirect_field_name=None)
def modal_remove_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.POST:
        produto.atualizado_por = request.user
        produto.ativo = False
        produto.save()
        return redirect(reverse('lista-produtos'))
    else:
        return render(request, 'modal_remove_produto.html', {'produto': produto})
