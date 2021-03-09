from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from controle_usuarios.models import Funcionario



class HistoricoAtualizacaoPrecos(models.Model):
    ean = models.ForeignKey("controle_estoque.Produto", on_delete=models.CASCADE,
                            related_name='hist_atual_preco_produto')
    descricao = models.CharField(max_length=30)
    preco_compra = models.DecimalField(max_digits=6, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=6, decimal_places=2)
    motivo_alteracao_preco = models.CharField(max_length=300)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hist_atual_preco_criado_por',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ean.ean}'

    class Meta:
        verbose_name = 'Historico de Atualização de Preços'
        verbose_name_plural = 'Historico de Atualização de Preços'
        ordering = ['-criado_em']


class VendaItem(models.Model):
    produto = models.ForeignKey("controle_estoque.Produto", on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_compra


STATUS_CHOICES = (
    (1, 'Pendente'),
    (2, 'Cancelada'),
    (3, 'Concluída'),
)


PAGAMENTO_CHOICES = (
    (1, 'Debito'),
    (2, 'Credito'),
    (3, 'Dinheiro'),
    (4, 'PicPay'),
    (5, 'Pix'),
)


class Venda(models.Model):
    produtos = models.ManyToManyField(VendaItem)
    valor_total_venda = models.DecimalField('Valor Total da Venda', decimal_places=2, max_digits=12, default=0)
    descricao = models.TextField('Descrição da Venda', max_length=150, blank=True, null=True)
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    criado_em = models.DateTimeField('Venda Realizada Em', auto_now_add=True)
    status = models.SmallIntegerField('Status', choices=STATUS_CHOICES, default=1)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendas_criadopor',
                                   editable=False)
    caixa = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vendas_caixa',
                              verbose_name='Operador/Caixa')
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vendas_vendedor',
                                 verbose_name="Vendedor")
    desconto = models.DecimalField('Desconto', decimal_places=2, max_digits=12, default=0,
                                   help_text="Digite o valor de desconto da venda, exemplo R$ 10,00")
    forma_pagto = models.SmallIntegerField("Forma De Pagamento", choices=PAGAMENTO_CHOICES)
    cpf = models.CharField("CPF", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        try:
            return f'Pedido {self.id} - {self.criado_em.strftime("%d/%m/%Y - %H:%M:%S")}'
        except AttributeError:
            return f'Pedido {self.id} - {self.criado_em}'

    def calc_total(self):
        total = 0
        for order_item in self.produtos.all():
            total += order_item.get_total_preco_produto()
        self.valor_total_venda = total - self.desconto
        return self.valor_total_venda

    def save(self, *args, **kwargs):
        try:
            self.calc_total()
            super(Venda, self).save(*args, **kwargs)
        except ValueError:
            super(Venda, self).save(*args, **kwargs)


class HistoricoVendas(models.Model):
    vendas = models.ForeignKey(Venda, on_delete=models.CASCADE)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default='Concluída')
    valor_total_diario = models.DecimalField(max_digits=6, decimal_places=2)
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="historico_vendedor")
    caixa = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name="historico_caixa")
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name="historico_criado",
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Venda'
        verbose_name_plural = 'Histórico de Vendas'
        ordering = ['-criado_em']
