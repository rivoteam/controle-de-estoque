from django.db import models
from django.contrib.auth.models import User
from controle_usuarios.models import Funcionario
from core.utils import STATUS_VENDA_CHOICES, PAGAMENTO_CHOICES


class CarrinhoVenda(models.Model):
    produto = models.ForeignKey("controle_estoque.Produto", on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField(default=1)
    venda = models.ForeignKey("Venda", on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_venda


class Venda(models.Model):
    descricao = models.TextField('Descrição da Venda', max_length=150, blank=True, null=True)
    status = models.SmallIntegerField('Status', choices=STATUS_VENDA_CHOICES, default=1)
    caixa = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, related_name='vendas_caixa',
                              verbose_name='Operador/Caixa', help_text="Caixa que está efetuando a venda")
    vendedor = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, related_name='vendas_vendedor',
                                 verbose_name="Vendedor", help_text="Vendedor que atendeu o cliente")
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    cpf = models.CharField("CPF", max_length=30, null=True, blank=True)
    desconto = models.DecimalField('Desconto', decimal_places=2, max_digits=12, default=0,
                                   help_text="Digite o valor de desconto da venda, exemplo R$ 10,00")
    forma_pagto = models.SmallIntegerField("Forma De Pagamento", choices=PAGAMENTO_CHOICES)
    valor_total_venda = models.DecimalField('Valor Total da Venda', decimal_places=2, max_digits=12, default=0)
    criado_em = models.DateTimeField('Venda Realizada Em', auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='vendas_criadopor', editable=False)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def __str__(self):
        try:
            return f'Venda {self.id} - {self.criado_em.strftime("%d/%m/%Y - %H:%M:%S")}'
        except AttributeError:
            return f'Venda {self.id} - {self.criado_em}'

    def calc_total(self):
        total = 0
        for order_item in CarrinhoVenda.objects.filter(venda_id=self.id):
            total += order_item.get_total_preco_produto()
        self.valor_total_venda = total - self.desconto
        return self.valor_total_venda

    def save(self, *args, **kwargs):
        try:
            self.calc_total()
            super(Venda, self).save(*args, **kwargs)
        except ValueError:
            super(Venda, self).save(*args, **kwargs)

    def get_produtos_vendidos(self):
        queryset = []
        for produto in CarrinhoVenda.objects.filter(venda=self):
            queryset.append(produto.produto)
        return queryset

    # def get_produtos_vendidos(self):
    #     return [produto.produto for produto in CarrinhoVenda.objects.filter(venda=self)]

    def get_valores_produtos_vendidos(self):
        queryset = {}
        for produto in CarrinhoVenda.objects.filter(venda=self):
            queryset.update({"produto": produto.produto, "preco": produto.produto.preco_venda})
        return queryset


class HistoricoVendas(models.Model):
    vendas = models.ForeignKey(Venda, on_delete=models.DO_NOTHING)
    status = models.SmallIntegerField(choices=STATUS_VENDA_CHOICES, default='Concluída')
    valor_total_diario = models.DecimalField(max_digits=6, decimal_places=2)
    vendedor = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, related_name="historico_vendedor")
    caixa = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, related_name="historico_caixa")
    criado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="historico_criado",
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Venda'
        verbose_name_plural = 'Histórico de Vendas'
        ordering = ['-criado_em']
