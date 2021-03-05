from django.contrib import admin
from .models import HistoricoVendas, HistoricoAtualizacaoPrecos, Venda, VendaItem
from controle_estoque.utils import export_as_csv, export_xlsx, salva_criado_por


@admin.register(HistoricoVendas)
class HistoricoVendasAdmin(admin.ModelAdmin):
    list_display = ['id', 'itens_compra', 'status', 'valor_compra', 'vendedor', 'caixa', 'criado_por', 'criado_em', ]
    search_fields = ['id', 'itens_compra', 'status', 'valor_compra', 'vendedor', 'caixa', 'criado_por', 'criado_em', ]
    list_filter = ['itens_compra', 'status', 'valor_compra', 'vendedor', 'caixa', 'criado_por', 'criado_em', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


@admin.register(HistoricoAtualizacaoPrecos)
class HistoricoAtualizacaoPrecosAdmin(admin.ModelAdmin):
    list_display = ['id', 'ean', 'descricao', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'criado_por',
                    'criado_em']
    search_fields = ['id', 'ean', 'descricao', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'criado_por',
                     'criado_em', ]
    list_filter = ['ean', 'descricao', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'criado_por',
                   'criado_em', ]

    actions = (export_as_csv, export_xlsx)

# @admin.register(Venda)
# class VendaAdmin(admin.ModelAdmin):
#     list_display = ['id', 'preco_venda', 'descricao', 'nota_fiscal', 'data_venda', 'status', 'criado_por',]
#     search_fields = ['id', 'preco_venda', 'descricao', 'nota_fiscal', 'data_venda', 'status', 'criado_por',]
#     list_filter = ['preco_venda', 'descricao', 'nota_fiscal', 'data_venda', 'status', 'criado_por', ]
#
#     actions = (export_as_csv, export_xlsx)
#
#     def save_model(self, request, obj, form, change):
#         salva_criado_por(request, obj)

admin.site.register(Venda)
admin.site.register(VendaItem)
