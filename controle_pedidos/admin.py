from django.contrib import admin
from .models import PedidoCompra, CarrinhoPedido
from core.utils import salva_criado_por

admin.site.register(CarrinhoPedido)


@admin.register(PedidoCompra)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ["fornecedor", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                    "criado_por"]
    search_fields = ["fornecedor", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                     "criado_por"]
    list_filter = ["fornecedor", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                   "criado_por"]

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)
