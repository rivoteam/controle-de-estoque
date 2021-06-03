from django.db import models
from django.contrib.auth.models import User
from controle_estoque.models import Produto
from core.utils import STATUS_COMPRA_CHOICES


class CarrinhoPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    pedidocompra = models.ForeignKey("PedidoCompra", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_compra


class PedidoCompra(models.Model):
    fornecedor = models.ForeignKey('controle_estoque.Fornecedor', on_delete=models.PROTECT, related_name='pedidos')
    preco_pedido = models.DecimalField('Preço Total do Pedido', decimal_places=2, max_digits=12, default=0)
    descricao = models.CharField('Descrição do Pedido', max_length=50, blank=True, null=True)
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    data_pedido = models.DateTimeField('Pedido Realizado Em', auto_now_add=True)
    status = models.SmallIntegerField('Status', choices=STATUS_COMPRA_CHOICES, default=1)
    ativo = models.BooleanField(default=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedido_criadopor',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.PROTECT,
                                       related_name='pedido_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    csv_compra = models.FileField(upload_to='pedidos_gerados/', null=True, blank=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-id']

    def __str__(self):
        return f'Pedido {self.id}'

    def calc_total(self):
        total = 0
        for order_item in CarrinhoPedido.objects.filter(pedidocompra_id=self.id):
            total += order_item.get_total_preco_produto()
        return total

    def save(self, *args, **kwargs):
        self.preco_pedido = self.calc_total()
        super(PedidoCompra, self).save(*args, **kwargs)

    def get_produtos_comprados(self):
        queryset = []
        for produto in CarrinhoPedido.objects.filter(pedidocompra=self):
            queryset.append(produto.produto)
        return queryset

    def get_valores_produtos_comprados(self):
        queryset = {}
        for produto in CarrinhoPedido.objects.filter(pedidocompra=self):
            queryset.update({"produto": produto.produto, "preco": produto.produto.preco_compra})
        return queryset

    def get_len_produtos_comprados(self):
        quantidade = 0
        for produto in CarrinhoPedido.objects.filter(pedidocompra=self):
            quantidade += produto.quantidade
        return quantidade