from django.contrib import admin
from .models import Venda, CarrinhoVenda
from core.utils import export_as_csv, export_xlsx, salva_criado_por


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'valor_total_venda', 'descricao', 'nota_fiscal', 'criado_em', 'status', 'criado_por', 'caixa',
                    'vendedor', 'desconto', 'forma_pagto', 'cpf']
    search_fields = ['id', 'valor_total_venda', 'descricao', 'nota_fiscal', 'criado_em', 'status', 'criado_por',
                     'caixa', 'vendedor', 'desconto', 'forma_pagto', 'cpf', ]
    list_filter = ['valor_total_venda', 'descricao', 'nota_fiscal', 'criado_em', 'status', 'criado_por', 'caixa',
                   'vendedor', 'desconto', 'forma_pagto', 'cpf', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)


admin.site.register(CarrinhoVenda)
