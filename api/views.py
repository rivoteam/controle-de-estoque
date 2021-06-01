from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from controle_estoque.models import Produto, Fornecedor
from controle_usuarios.models import Funcionario
from controle_pedidos.models import PedidoCompra, CarrinhoPedido
from controle_vendas.models import Venda, CarrinhoVenda
from .serializers import ProdutoSerializer, PedidoSerializer, CarrinhoPedidoSerializer, VendaSerializer, \
    CarrinhoVendaSerializer
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.conf import settings
from core.utils import send_csv_compra
import os


def api_home(request):
    return JsonResponse({"Reposta": "Homepage da API, criado para utilizar parametros de URL do Django"}, safe=False)


class ProdutoListApi(ListAPIView):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (IsAuthenticated,)


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = (IsAuthenticated,)


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = (IsAuthenticated,)


class CarrinhoPedidoViewSet(viewsets.ModelViewSet):
    queryset = CarrinhoPedido.objects.all()
    serializer_class = CarrinhoPedidoSerializer
    permission_classes = (IsAuthenticated,)


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer
    permission_classes = (IsAuthenticated,)


class CarrinhoVendaViewSet(viewsets.ModelViewSet):
    queryset = CarrinhoVenda.objects.all()
    serializer_class = CarrinhoVendaSerializer
    permission_classes = (IsAuthenticated,)


@login_required
def get_detail_produtos(request, pk):
    try:
        produto = Produto.objects.get(ean=pk)
        serializer = ProdutoSerializer(produto)
        return JsonResponse(serializer.data, status=200, safe=False)
    except:
        return JsonResponse('Nao encontrado', status=404, safe=False)


@require_http_methods("POST")
@csrf_exempt
@login_required
def post_realiza_vendas(request):
    produtos_json = json.loads(request.body)
    vendedor = Funcionario.objects.get(id=int(produtos_json['vendedor']))
    instance_venda = Venda.objects.create(caixa=request.user.funcionario, vendedor=vendedor,
                                          forma_pagto=int(produtos_json['forma_pgto']), criado_por=request.user,
                                          status=3, cpf=produtos_json['numerocpf'])
    for produto_json in produtos_json['produtos']:
        produto = Produto.objects.get(id=produto_json['produto']['id'])
        CarrinhoVenda.objects.create(produto=produto, quantidade=int(produto_json['quantidade']),
                                     venda=instance_venda)
    return JsonResponse({"Requisicao": f"Venda registrada {instance_venda}"}, status=200, safe=False)


@require_http_methods("POST")
@csrf_exempt
@login_required
def post_realiza_compras(request):
    fornecedor_temp_list = []
    compra = []

    produtos_json = json.loads(request.body)
    for produto_json in produtos_json['produtos']:
        fornecedor_temp_list.append(int(produto_json['produto']['fornecedor']))
    fornecedor_temp_list = set(fornecedor_temp_list)
    for fornecedor in fornecedor_temp_list:
        valor_compra = 0
        fornecedor_obj = Fornecedor.objects.get(id=fornecedor)
        instance_pedido = PedidoCompra.objects.create(fornecedor=fornecedor_obj, criado_por=request.user)
        for produto_json in produtos_json['produtos']:
            if produto_json['produto']['fornecedor'] == fornecedor_obj.id:
                produto = Produto.objects.get(id=int(produto_json['produto']['id']))
                valor_compra += (produto.preco_compra * int(produto_json['quantidade']))
                compra.append({"produto": produto.ean, "tamanho": produto.tamanho,
                               "quantidade": int(produto_json['quantidade'])})
                CarrinhoPedido.objects.create(quantidade=int(produto_json['quantidade']), produto_id=produto.id,
                                              pedidocompra=instance_pedido)
                produto.em_compra = True
                produto.save()
        if valor_compra >= fornecedor_obj.faturamento_minimo:
            file_df = pd.DataFrame(data=compra)
            pasta_pedidos = os.path.join(settings.BASE_DIR, 'controle_pedidos/pedidos_gerados')
            file_name = f'{pasta_pedidos}/compra-pedido-{instance_pedido.id}.csv'
            file_df.to_csv(file_name, index=False)
            send_csv_compra(file_name, fornecedor_obj.email)
            instance_pedido.status = 3
            instance_pedido.save()
    return JsonResponse({"Requisicao": f"Compra registrada "}, status=200, safe=False)
