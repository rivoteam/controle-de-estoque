from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from controle_pedidos.models import CarrinhoPedido, PedidoCompra
from controle_vendas.models import Venda, CarrinhoVenda
from controle_estoque.models import Produto


@receiver(post_save, sender=CarrinhoPedido)
def post_save_pedido_compra(sender, created, instance, **kwargs):
    pedido = PedidoCompra.objects.get(pk=instance.pedidocompra.id)
    pedido.save()


@receiver(post_save, sender=PedidoCompra)
def post_save_atualiza_estoque(sender, created, instance, **kwargs):
    if instance.status == 5:
        list_produtos = CarrinhoPedido.objects.filter(pedidocompra=instance)
        for produto_comprado in list_produtos:
            produto = Produto.objects.get(pk=produto_comprado.produto_id)
            produto.total_pecas += produto_comprado.quantidade
            produto.save()
    return


@receiver(post_save, sender=CarrinhoVenda)
def post_save_venda(sender, created, instance, **kwargs):
    venda = Venda.objects.get(pk=instance.venda.id)
    venda.save()
    if venda.status == 3:
        produto = Produto.objects.get(pk=instance.produto.id)
        produto.total_pecas -= instance.quantidade
        produto.save()
    return
