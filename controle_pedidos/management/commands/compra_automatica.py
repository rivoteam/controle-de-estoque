from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from controle_pedidos.models import PedidoCompra, CarrinhoPedido
from controle_estoque.models import Produto, Fornecedor
from django.conf import settings
import os
import pandas as pd
from core.utils import send_csv_compra


def compra_automatica_produtos():
    """
    Realiza compra automática de produtos em alerta minimo
    """
    produtos_em_alerta = Produto.objects.filter(ativo=True, limite_alerta_min=False, em_compra=False, auto_pedido=True)
    temp_list = []
    for produto in produtos_em_alerta:
        temp_list.append(produto.fornecedor)
    fornecedores_instance = list(set(temp_list))

    for fornecedor in fornecedores_instance:
        fornecedor_obj = Fornecedor.objects.get(id=fornecedor.id)
        defaults = {"fornecedor": fornecedor_obj, "criado_por": User.objects.get(username='robo'),
                    "atualizado_por": User.objects.get(username='robo')}
        pedido, created = PedidoCompra.objects.get_or_create(fornecedor=fornecedor_obj, status=1, defaults=defaults,
                                                             descricao="Pedido gerado automaticamente")
        compra = []
        for produto in produtos_em_alerta:
            if produto.fornecedor == fornecedor_obj:
                compra.append({"produto": produto.ean, "tamanho": produto.tamanho,
                               "quantidade": (produto.min_pecas - produto.total_pecas)})
                defaults = {"quantidade": (produto.min_pecas - produto.total_pecas), "produto": produto,
                            "pedidocompra": pedido}
                CarrinhoPedido.objects.get_or_create(quantidade=(produto.min_pecas - produto.total_pecas),
                                                     produto=produto, pedidocompra=pedido, defaults=defaults)
                if pedido.preco_pedido >= fornecedor_obj.faturamento_minimo:
                    produto.em_compra = True
                    produto.save()
        pedido.save()
        if pedido.preco_pedido >= fornecedor_obj.faturamento_minimo:
            file_df = pd.DataFrame(data=compra)
            file_name = f'compra-pedido-{pedido.id}.csv'
            file_df.to_csv(file_name, index=False)
            pedido.csv_compra = file_name
            pedido.status = 3
            pedido.save()
            send_csv_compra(file_name, fornecedor_obj.email)
        return


class Command(BaseCommand):
    help = 'Envia e-mails de compras automaticamente'

    def handle(self, *args, **options):
        compra_automatica_produtos()
