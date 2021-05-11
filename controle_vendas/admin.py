from django.contrib import admin
from .models import Venda, CarrinhoVenda
from core.utils import export_as_csv, export_xlsx, salva_criado_por


@admin.register(CarrinhoVenda)
class CarrinhoVendaAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'venda']


class CarrinhoVendaInLine(admin.TabularInline):
    model = CarrinhoVenda
    extra = 0


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    inlines = [CarrinhoVendaInLine]
    list_display = ['id', "ativo", 'valor_total_venda', 'descricao', 'nota_fiscal', 'criado_em', 'status', 'criado_por',
                    'caixa', 'vendedor', 'desconto', 'forma_pagto', 'cpf']
    search_fields = ["id", "ativo", 'descricao', 'criado_em', 'status', 'criado_por__username', 'cpf', 'nota_fiscal',
                     'caixa__cargo_funcionario', 'vendedor__cargo_funcionario', 'desconto', 'forma_pagto']
    list_filter = ["ativo", 'valor_total_venda', 'descricao', 'nota_fiscal', 'criado_em', 'status', 'criado_por',
                   'caixa', 'vendedor', 'desconto', 'forma_pagto', 'cpf', ]

    actions = (export_as_csv, export_xlsx)

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)
