from django.urls import path
from .views import detalhe_produto, lista_produtos, modal_remove_produto, modal_cria_produto, modal_atualiza_produto

urlpatterns = [
    path('lista-produtos/', lista_produtos, name="lista-produtos"),
    path('detalhe-produto/<int:pk>', detalhe_produto, name='detalhe_produto'),
    path("modal-cria-produto/", modal_cria_produto, name="modal-cria-produto"),
    path('modal-atualiza-produto/<int:pk>', modal_atualiza_produto, name='modal-atualiza-produto'),
    path('modal-remove-produto/<int:pk>', modal_remove_produto, name='modal-remove-produto'),
]
