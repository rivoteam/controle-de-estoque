from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # visualizar img
from django.conf.urls.static import static  # visualizar img

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('interfaces.urls')),
    path('api-rest/', include('api.urls')),
    path('vendas/', include('controle_vendas.urls')),
    path('pedidos/', include('controle_pedidos.urls')),
    path('produtos/', include('controle_estoque.urls')),
]
