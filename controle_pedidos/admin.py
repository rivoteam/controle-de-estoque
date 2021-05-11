from django.contrib import admin
from .models import PedidoCompra, CarrinhoPedido
from core.utils import salva_criado_por


@admin.register(CarrinhoPedido)
class CarrinhoPedidoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'pedidocompra']


class CarrinhoPedidoInLine(admin.TabularInline):
    model = CarrinhoPedido
    extra = 0


@admin.register(PedidoCompra)
class PedidoAdmin(admin.ModelAdmin):
    inlines = [CarrinhoPedidoInLine]
    list_display = ["id", "fornecedor", "ativo", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                    "criado_por", "criado_em", "atualizado_por", "atualizado_em"]
    search_fields = ["id", "fornecedor__nome_empresa", "ativo", "preco_pedido", "descricao", "nota_fiscal", "data_pedido",
                     "status", "criado_por__username", "criado_em", "atualizado_por__username", "atualizado_em"]
    list_filter = ["data_pedido", "fornecedor", "ativo", "status", "criado_por", "criado_em", "atualizado_por",
                   "atualizado_em", "nota_fiscal", "descricao"]

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)
