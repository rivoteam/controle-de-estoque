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


class HistoricoVendas(models.Model):
    itens_compra = models.JSONField(default=dict)
    status = models.CharField(max_length=30, choices=VENDAS_STATUS, default='Concluída')
    valor_compra = models.DecimalField(max_digits=6, decimal_places=2)
    vendedor = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='cargo_vendedor')
    caixa = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='cargo_caixa')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hist_vendas_criado_por',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Histórico de Venda'
        verbose_name_plural = 'Histórico de Vendas'
        ordering = ['-criado_em']
