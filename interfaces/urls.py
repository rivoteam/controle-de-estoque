from django.urls import path
from .views import homepage, detalhe_produto, lista_produtos, user_logout, modal_remove_produto, modal_cria_produto, \
    modal_atualiza_produto

urlpatterns = [
    path('', homepage, name="homepage"),
    path('logout/', user_logout, name="logout"),

    # Listagem
    path('lista-produtos/', lista_produtos, name="lista-produtos"),

    # Criação
    path("modal-cria-produto/", modal_cria_produto, name="modal-cria-produto"),

    # Detalhes
    path('detalhe-produto/<int:pk>', detalhe_produto, name='detalhe_produto'),

    # Remoção
    path('modal-remove-produto/<int:pk>', modal_remove_produto, name='modal-remove-produto'),

    # Atualização
    path('modal-atualiza-produto/<int:pk>', modal_atualiza_produto, name='modal-atualiza-produto'),
]
