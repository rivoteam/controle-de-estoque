from django.db.models.signals import post_save
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


@receiver(post_save, sender=Produto)
def post_save_ean_sku(sender, created, instance, **kwargs):
    produto = Produto.objects.get(pk=instance.id)

    if created:
        motivo = produto.motivo_alteracao_preco
        tamanho_sku = f"{(2 - len(produto.tamanho)) * '0'}{produto.tamanho}"
        produto.limite_alerta_min = False if produto.total_pecas <= produto.alerta_min else True
        produto.motivo_alteracao_preco = None
        produto.ean = generate_barcode(self=produto.id) if not produto.ean else produto.ean
        produto.sku = f"{produto.genero[:1]}{produto.categoria.codigo}{produto.subcategoria.codigo}{tamanho_sku}".upper()
        produto.save()

        produto_salvo = Produto.objects.filter(ean=produto.ean).first()
        historico = HistoricoAtualizacaoPrecos.objects.filter(produto=produto_salvo).first()

        if ((historico and produto_salvo) and ((historico.preco_compra != produto_salvo.preco_compra) or (
                historico.preco_venda != produto_salvo.preco_venda))) or produto_salvo and not historico:
            HistoricoAtualizacaoPrecos.objects.create(
                produto=produto_salvo,
                descricao=produto.descricao,
                preco_compra=produto.preco_compra,
                preco_venda=produto.preco_venda,
                motivo_alteracao_preco=motivo,
                criado_por=produto.criado_por
            )

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
