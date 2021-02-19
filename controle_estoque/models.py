from django.db import models
from django.contrib.auth.models import User
from random import randint
from controle_usuarios.models import ESTADOS_CHOICES
from controle_vendas.models import HistoricoAtualizacaoPrecos


class Fornecedor(models.Model):
    nome_empresa = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=15)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=300)
    pessoa_contato = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fornecedor_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fornecedor_atualizado_por',
                                       editable=False,
                                       null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=100, choices=ESTADOS_CHOICES, default='SP')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_empresa

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome_empresa']


class Genero(models.Model):
    genero = models.CharField(max_length=15)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genero_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='genero_atualizado_por',
                                       editable=False,
                                       null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.genero}'

    class Meta:
        verbose_name = 'Gênero'
        verbose_name_plural = 'Gêneros'
        ordering = ['genero']


class Categoria(models.Model):
    categoria = models.CharField(max_length=30)
    codigo = models.CharField(max_length=3)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categoria_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categoria_atualizado_por',
                                       editable=False,
                                       null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.categoria}'

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['categoria']


class Subcategoria(models.Model):
    subcategoria = models.CharField(max_length=30)
    codigo = models.CharField(max_length=3)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcategoria_criado_por',
                                   editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcategoria_atualizado_por',
                                       editable=False,
                                       null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subcategoria}'

    def save(self, *args, **kwargs):
        subcategorias = Subcategoria.objects.all()
        codigos = [i.codigo for i in subcategorias]
        if not self.codigo in codigos:
            super(Subcategoria, self).save(*args, **kwargs)
        else:
            self.codigo = 'NUL'
            super(Subcategoria, self).save()

    class Meta:
        verbose_name = 'Subcategoria'
        verbose_name_plural = 'Subcategorias'
        ordering = ['subcategoria']


class TamanhoProduto(models.Model):
    tamanho = models.CharField(max_length=2)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tamanho_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='tamanho_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.tamanho}'

    class Meta:
        verbose_name = 'Tamanho do Produto'
        verbose_name_plural = 'Tamanho dos Produtos'
        ordering = ['tamanho']


class Produto(models.Model):
    descricao = models.CharField(max_length=50)
    genero = models.ForeignKey("Genero", on_delete=models.CASCADE)
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE)
    subcategoria = models.ForeignKey("Subcategoria", on_delete=models.CASCADE)
    tamanho = models.ForeignKey("TamanhoProduto", on_delete=models.PROTECT)
    cor = models.CharField(max_length=30)
    grade = models.CharField(max_length=30)
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
    fornecedor = models.ForeignKey("Fornecedor", on_delete=models.CASCADE)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='produto_criado_por', editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_por = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='produto_atualizado_por', editable=False, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.ean}'

    def generate_barcode(self):
        '''
        Se não encontrar esse code_id no DB atribui o code_id ao produto
        Se já existir gera outro code_id
        '''
        code_id = str(randint(7890000000000, 7899999999999))
        return code_id

    def save(self, *args, **kwargs):
        motivo = self.motivo_alteracao_preco

        tamanho_sku = f"{self.tamanho}{(2 - len(self.tamanho.tamanho)) * '0'}"
        self.limite_alerta_min = False if self.total_pecas <= self.alerta_min else True
        self.motivo_alteracao_preco = None
        self.ean = self.generate_barcode() if not self.ean else self.ean
        self.sku = f"{self.genero.genero[:1]}{self.categoria.codigo}{self.subcategoria.codigo}{tamanho_sku}"
        super(Produto, self).save(*args, **kwargs)

        p = Produto.objects.filter(ean=self.ean).first()
        h = HistoricoAtualizacaoPrecos.objects.filter(ean=p).first()
        if ((h and p) and ((h.preco_compra != p.preco_compra) or (h.preco_venda != p.preco_venda))) or p and not h:
            HistoricoAtualizacaoPrecos.objects.create(
                ean=p,
                descricao=self.descricao,
                preco_compra=self.preco_compra,
                preco_venda=self.preco_venda,
                motivo_alteracao_preco=motivo,
                criado_por=self.criado_por
            )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']
