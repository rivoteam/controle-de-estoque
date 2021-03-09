from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from controle_estoque.models import Produto

STATUS_CHOICES = (
    (1, 'Gerado'),
    (2, 'Em separação'),
    (3, 'Enviado'),
    (4, 'Concluído'),
)


class PedidoItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_compra


class Pedido(models.Model):
    fornecedor = models.ForeignKey('controle_estoque.Fornecedor', on_delete=models.CASCADE, related_name='pedidos')
    produtos = models.ManyToManyField(PedidoItem)
    preco_pedido = models.DecimalField('Preço Total do Pedido', decimal_places=2, max_digits=12, default=0)
    descricao = models.TextField('Descrição do Pedido', max_length=150, blank=True, null=True)
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    data_pedido = models.DateTimeField('Pedido Realizado Em', auto_now_add=True)
    status = models.SmallIntegerField('Status', choices=STATUS_CHOICES, default=1)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedido_criadopor',
                                   editable=False)
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        try:
            return f'Pedido {self.id} - {self.data_pedido.strftime("%d/%m/%Y - %H:%M:%S")}'
        except AttributeError:
            return f'Pedido {self.id} - {self.data_pedido}'

    def calc_total(self):
        total = 0
        for order_item in self.produtos.all():
            total += order_item.get_total_preco_produto()
        self.preco_pedido = total
        return self.preco_pedido

    def save(self, *args, **kwargs):
        try:
            self.calc_total()
            super(Pedido, self).save(*args, **kwargs)
        except ValueError:
            super(Pedido, self).save(*args, **kwargs)
