from django.contrib import admin
from .models import Fornecedor, Categoria, Subcategoria, Produto, HistoricoAtualizacaoPrecos
from core.utils import export_as_csv, export_xlsx, salva_criado_por


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_empresa', 'cnpj', 'endereco', 'ativo']
    search_fields = ['id', 'nome_empresa', 'endereco', 'ativo']
    list_filter = ['nome_empresa', 'cnpj', 'ativo']

    actions = (export_as_csv, export_xlsx)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria', 'codigo']
    search_fields = ['id', 'categoria', 'codigo']
    list_filter = ['categoria', 'codigo']

    actions = (export_as_csv, export_xlsx)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'subcategoria', 'codigo']
    search_fields = ['id', 'subcategoria', 'codigo']
    list_filter = ['subcategoria', 'codigo']

    actions = (export_as_csv, export_xlsx)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', "ativo", 'descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas',
                    'alerta_min', 'limite_alerta_min', 'total_pecas', 'preco_compra', 'preco_venda',
                    'motivo_alteracao_preco', 'auto_pedido', 'ean',
                    'sku', 'fornecedor', 'criado_por', 'criado_em', 'atualizado_por', 'atualizado_em']

    search_fields = ['id', "ativo", 'descricao', 'genero', 'tamanho', 'cor', 'alerta_min', 'limite_alerta_min',
                     'motivo_alteracao_preco', 'auto_pedido', 'ean', 'sku', 'categoria__categoria',
                     'subcategoria__subcategoria', 'fornecedor__nome_empresa', 'criado_por__username',
                     'atualizado_por__username', 'criado_em', 'atualizado_em']

    list_filter = ["ativo", 'genero', 'categoria', 'subcategoria', 'limite_alerta_min', 'auto_pedido', 'criado_por',
                   'criado_em', 'atualizado_por', 'atualizado_em', 'fornecedor', 'cor', 'tamanho', 'ean', 'sku',
                   'descricao']

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


export_xlsx.short_description = "Exportar dados em formato Excel"
export_as_csv.short_description = "Exportar dados em formato CSV"


@admin.register(HistoricoAtualizacaoPrecos)
class HistoricoAtualizacaoPrecosAdmin(admin.ModelAdmin):
    list_display = ['id', 'produto', 'descricao', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'criado_por',
                    'criado_em']
    search_fields = ['id', 'produto__ean', 'descricao', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco',
                     'criado_por__username',
                     'criado_em']
    list_filter = ['motivo_alteracao_preco', 'criado_por', 'criado_em', 'produto', 'descricao']

    actions = (export_as_csv, export_xlsx)
