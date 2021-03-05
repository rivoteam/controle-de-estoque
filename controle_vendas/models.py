from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from controle_usuarios.models import Funcionario

VENDAS_STATUS = (
    ('Concluída', 'Concluída'),
    ('Cancelada', 'Cancelada'),
)


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
    # produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_compra

STATUS_CHOICES = (
    (1, 'Gerado'),
    (2, 'Em separação'),
    (3, 'Enviado'),
    (4, 'Concluído'),
)

class Venda(models.Model):

    # fornecedor = models.ForeignKey('controle_estoque.Fornecedor', on_delete=models.CASCADE, related_name='pedidos')
    produtos = models.ManyToManyField(VendaItem)
    valor_total_venda = models.DecimalField('Valor Total da Venda', decimal_places=2, max_digits=12, default=0)
    descricao = models.TextField('Descrição da Venda', max_length=150, blank=True, null=True)
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    data_venda = models.DateTimeField('Venda Realizada Em', auto_now_add=True, editable=True)
    status = models.SmallIntegerField('Status', choices=STATUS_CHOICES, default=1)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    caixa = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='caixa')
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vendedor')
    # sub_total = models.DecimalField('Sub Total da Venda', decimal_places=2, max_digits=12, default=0)
    # desconto = models.DecimalField('Desconto', decimal_places=2, max_digits=12, default=0)
    forma_pagto = models.CharField("Forma De Pagamento", max_length=30)
    cpf = models.CharField("CPF", max_length=30)

    # def save(self, *args, **kwargs):
    #     self.desconto /= 100
    #     self.valor_total_venda = self.sub_total * self.desconto
    #     super(Venda, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        return f'{self.id} - {self.data_venda}'

    def calc_total(self):
        total = 0
        for order_item in self.produtos.all():
            total -= order_item.get_total_preco_produto()
        self.preco_venda = total
        return self.preco_venda

    def save(self, *args, **kwargs):
        try:
            self.calc_total()
            super(Venda, self).save(*args, **kwargs)
        except ValueError:
            super(Venda, self).save(*args, **kwargs)



class HistoricoVendas(models.Model):
    vendas = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='vendas')
    status = models.CharField(max_length=30, choices=VENDAS_STATUS, default='Concluída')
    valor_total_diario = models.DecimalField(max_digits=6, decimal_places=2)
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='cargo_vendedor')
    caixa = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='cargo_caixa')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hist_vendas_criado_por',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = 'Histórico de Venda'
        verbose_name_plural = 'Histórico de Vendas'
        ordering = ['-criado_em']


