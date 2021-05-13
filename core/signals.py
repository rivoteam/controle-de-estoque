from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from controle_pedidos.models import CarrinhoPedido, PedidoCompra
from controle_vendas.models import Venda, CarrinhoVenda
from controle_estoque.models import Produto, HistoricoAtualizacaoPrecos
from random import randint


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


def generate_barcode(self):
    code_id = str(randint(7890000000000, 7899999999999))
    if not Produto.objects.filter(ean=code_id).first() is None:
        self.generate_barcode()
    return code_id


@receiver(pre_save, sender=Produto)
def pre_save_product_data(sender, instance, **kwargs):
    tamanho_sku = f"{(2 - len(instance.tamanho)) * '0'}{instance.tamanho}"
    instance.limite_alerta_min = False if instance.total_pecas <= instance.alerta_min else True
    instance.ean = generate_barcode(self=instance.id) if not instance.ean else instance.ean
    instance.sku = f"{instance.genero[:1]}{instance.categoria.codigo}{instance.subcategoria.codigo}{tamanho_sku}".upper()
    filtro = Produto.objects.filter(sku__startswith=instance.sku)

    if len(filtro) == 0:
        instance.sku = f"{instance.genero[:1]}{instance.categoria.codigo}{instance.subcategoria.codigo}{tamanho_sku}00".upper()
    else:
        sku_final = int(max([f.sku for f in filtro])[-2:]) + 1
        novo_sku_final = f"{(2 - len(str(sku_final))) * '0'}{sku_final}"
        instance.sku += str(novo_sku_final)
    return


@receiver(post_save, sender=Produto)
def post_save_price_update_history(sender, instance, **kwargs):
    historico = HistoricoAtualizacaoPrecos.objects.filter(produto=instance).first()
    if ((historico and instance)
        and ((historico.preco_compra != instance.preco_compra)
             or (historico.preco_venda != instance.preco_venda))) \
            or instance and not historico:
        HistoricoAtualizacaoPrecos.objects.create(
            produto=instance,
            descricao=instance.descricao,
            preco_compra=instance.preco_compra,
            preco_venda=instance.preco_venda,
            motivo_alteracao_preco=instance.motivo_alteracao_preco,
            criado_por=instance.criado_por
        )
    Produto.objects.filter(pk=instance.pk).update(motivo_alteracao_preco=None)
    return

'''
produto_salvo = Busca o produto salvo acima
historico = Verifica na tabela HistoricoAtualizacaoPrecos se existe o histórico deste produto

if =  
     COMPARA ((Se existe produto em Produto AND o histórico em HistoricoAtualizacaoPrecos) AND 
     COMPARA ((se o preço_compra em historico é diferente (!=) do preco_compra em produto_salvo) 
     OR COMPARA (se preco_venda em historico é diferente (!=) do preco_venda do produto_salvo)))
     Resumindo, verifica se houve alteração em preco_compra ou preco_venda
     COMPARA se existe somente produto_salvo em Produto AND NOT existe historico
     Se não existir historico do produto, será criado ou caso exista será criado um novo historico
     para o produto
    
'''
