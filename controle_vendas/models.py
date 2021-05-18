from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from controle_usuarios.models import Funcionario
from core.utils import STATUS_VENDA_CHOICES, PAGAMENTO_CHOICES


class CarrinhoVenda(models.Model):
    produto = models.ForeignKey("controle_estoque.Produto", on_delete=models.PROTECT)
    quantidade = models.IntegerField(default=1)
    venda = models.ForeignKey("Venda", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.quantidade} peças de {self.produto.descricao}"

    def get_total_preco_produto(self):
        return self.quantidade * self.produto.preco_venda

    def get_total_faturado(self):
        return (self.quantidade * self.produto.preco_venda) - (self.quantidade * self.produto.preco_compra)


class Venda(models.Model):
    descricao = models.CharField('Descrição da Venda', max_length=50, blank=True, null=True)
    status = models.SmallIntegerField('Status', choices=STATUS_VENDA_CHOICES, default=1)
    caixa = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='venda_caixa',
                              verbose_name='Operador/Caixa', help_text="Caixa que está efetuando a venda")
    vendedor = models.ForeignKey(Funcionario, on_delete=models.PROTECT, related_name='venda_vendedor',
                                 verbose_name="Vendedor", help_text="Vendedor que atendeu o cliente")
    nota_fiscal = models.FileField('Nota Fiscal Eletronica', upload_to='controle_pedidos/NFE', blank=True, null=True)
    cpf = models.CharField('CPF', null=True, blank=True, max_length=11, help_text='Preencha o campo apenas com números.', validators=[
        RegexValidator(r'^\d{11,11}$', message='Por favor, não insira letras, " . " e " - " no campo abaixo.')])

    desconto = models.DecimalField('Desconto', decimal_places=2, max_digits=12, default=0,
                                   help_text="Digite o valor de desconto da venda, exemplo R$ 10,00")
    forma_pagto = models.SmallIntegerField("Forma De Pagamento", choices=PAGAMENTO_CHOICES)
    valor_total_venda = models.DecimalField('Valor Total da Venda', decimal_places=2, max_digits=12, default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField('Venda Realizada Em', auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='venda_criadopor', editable=False)
    atualizado_por = models.ForeignKey(User, on_delete=models.PROTECT,
                                       related_name='venda_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-id']

    def __str__(self):
        return f'{self.id}'

    def calc_total(self):
        total = 0
        for order_item in CarrinhoVenda.objects.filter(venda_id=self.id):
            total += order_item.get_total_preco_produto()
        return total

    def calc_faturamento(self):
        total = 0
        for order_item in CarrinhoVenda.objects.filter(venda_id=self.id):
            total += order_item.get_total_faturado()
        return total

    def save(self, *args, **kwargs):
        self.valor_total_venda = self.calc_total()
        super(Venda, self).save(*args, **kwargs)

    def get_produtos_vendidos(self):
        queryset = []
        for produto in CarrinhoVenda.objects.filter(venda=self):
            queryset.append(produto.produto)
        return queryset

    def get_valores_produtos_vendidos(self):
        queryset = {}
        for produto in CarrinhoVenda.objects.filter(venda=self):
            queryset.update({"produto": produto.produto, "preco": produto.produto.preco_venda})
        return queryset
