from django.db import models
from django.contrib.auth.models import User
from core.utils import GENERO_CHOICES, TAMANHO_CHOICES


class Fornecedor(models.Model):
    nome_empresa = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=15)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=300)
    pessoa_contato = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_empresa

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome_empresa']


class Categoria(models.Model):
    categoria = models.CharField(max_length=30, unique=True)
    codigo = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return f'{self.categoria}'

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['categoria']

    def save(self, *args, **kwargs):
        self.categoria = self.categoria.title()
        self.codigo = self.codigo.upper()
        super(Categoria, self).save(*args, **kwargs)



class Subcategoria(models.Model):
    subcategoria = models.CharField(max_length=30)
    codigo = models.CharField(max_length=3)

    def __str__(self):
        return f'{self.subcategoria}'

    # def save(self, *args, **kwargs):
    #     subcategorias = Subcategoria.objects.all()
    #     codigos = [subcategoria.codigo for subcategoria in subcategorias]
    #     if not self.codigo in codigos:
    #         super(Subcategoria, self).save(*args, **kwargs)
    #     else:
    #         self.codigo = 'NUL'
    #         super(Subcategoria, self).save()

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['subcategoria']

    def save(self, *args, **kwargs):
        self.subcategoria = self.subcategoria.title()
        self.codigo = self.codigo.upper()
        super(Subcategoria, self).save(*args, **kwargs)


class Produto(models.Model):
    descricao = models.CharField(max_length=50)
    genero = models.CharField(choices=GENERO_CHOICES, max_length=255)
    categoria = models.ForeignKey("Categoria", on_delete=models.DO_NOTHING)
    subcategoria = models.ForeignKey("Subcategoria", on_delete=models.DO_NOTHING)
    tamanho = models.CharField("Tamanho", choices=TAMANHO_CHOICES, max_length=5)
    cor = models.CharField(max_length=30)
    min_pecas = models.PositiveSmallIntegerField()
    alerta_min = models.PositiveSmallIntegerField()
    limite_alerta_min = models.BooleanField(default=False, editable=False)
    total_pecas = models.PositiveSmallIntegerField()
    preco_compra = models.DecimalField(max_digits=6, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=6, decimal_places=2)
    motivo_alteracao_preco = models.CharField(max_length=300, null=True)
    auto_pedido = models.BooleanField(default=False)
    ean = models.CharField(max_length=13, editable=False)
    sku = models.CharField(max_length=10, editable=False)
    fornecedor = models.ForeignKey("Fornecedor", on_delete=models.DO_NOTHING)
    criado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='produto_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                       related_name='produto_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.descricao} {self.tamanho} - ean: {self.ean}'.title()

    def save(self, *args, **kwargs):
        super(Produto, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']


class HistoricoAtualizacaoPrecos(models.Model):
    produto = models.ForeignKey("controle_estoque.Produto", on_delete=models.DO_NOTHING,
                                related_name='hist_preco_produto')
    descricao = models.CharField(max_length=30)
    preco_compra = models.DecimalField(max_digits=6, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=6, decimal_places=2)
    motivo_alteracao_preco = models.CharField(max_length=300)
    criado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hist_preco_criado_por',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                       related_name='hist_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.produto.ean}'

    class Meta:
        verbose_name = 'Historico de Atualização de Preços'
        verbose_name_plural = 'Historico de Atualização de Preços'
        ordering = ['-criado_em']
