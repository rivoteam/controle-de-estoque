from django.contrib import admin
from .models import Pedido, PedidoItem
from controle_estoque.utils import salva_criado_por

# admin.site.register(Pedido)
admin.site.register(PedidoItem)


@admin.register(Pedido)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ["fornecedor", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                    "criado_por"]
    search_fields = ["fornecedor", "produtos", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                     "criado_por"]
    list_filter = ["fornecedor", "produtos", "preco_pedido", "descricao", "nota_fiscal", "data_pedido", "status",
                   "criado_por"]

    def save_model(self, request, obj, form, change):
        salva_criado_por(request, obj)
