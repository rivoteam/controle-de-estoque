from django.contrib import admin
from .models import Fornecedor, Genero, Categoria, Subcategoria, Produto, TamanhoProduto
from .utils import export_xlsx, export_as_csv, salva_criado_por


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_empresa', 'cnpj', 'endereco', 'estado', 'ativo', 'criado_por', 'criado_em',
                    'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'nome_empresa', 'endereco', 'estado', 'ativo', 'criado_por', 'criado_em', 'atualizado_por',
                     'atualizado_em', ]
    list_filter = ['nome_empresa', 'cnpj', 'estado', 'ativo', 'criado_por', 'criado_em', 'atualizado_por',
                   'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ['id', 'genero', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'genero', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    list_filter = ['genero', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'categoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    list_filter = ['categoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'subcategoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'subcategoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    list_filter = ['subcategoria', 'codigo', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(TamanhoProduto)
class TamanhoProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tamanho', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'tamanho', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    list_filter = ['tamanho', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'grade',
                    'min_pecas', 'alerta_min', 'limite_alerta_min', 'total_pecas', 'preco_compra', 'preco_venda',
                    'motivo_alteracao_preco', 'auto_pedido', 'ean',
                    'sku', 'fornecedor', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em', ]
    search_fields = ['id', 'descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'grade',
                     'alerta_min', 'limite_alerta_min', 'motivo_alteracao_preco', 'auto_pedido', 'ean', 'sku',
                     'fornecedor', 'criado_por', 'criado_em',
                     'atualizado_por', 'atualizado_em', ]
    list_filter = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'grade',
                   'alerta_min', 'limite_alerta_min', 'motivo_alteracao_preco', 'auto_pedido', 'ean', 'sku',
                   'fornecedor', 'criado_por', 'criado_em',
                   'atualizado_por', 'atualizado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


export_xlsx.short_description = "Exportar dados em formato Excel"
export_as_csv.short_description = "Exportar dados em formato CSV"
