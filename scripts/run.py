"""
Feito para testar em desenvolvimento e popular banco de todos
Instruções:
Copiar Código e colar no shell do Python Manage.py Shell
"""

from controle_estoque.models import Produto, Categoria, Subcategoria, Fornecedor
from django.contrib.auth.models import User
from random import randint

def run():
    categorias = [
        Categoria(categoria="Camiseta", codigo="CAT"),
        Categoria(categoria="Calca", codigo="CAL"),
        Categoria(categoria="Tenis", codigo="TEN"),
        Categoria(categoria="Blusa", codigo="BLU"),
        Categoria(categoria="Regata", codigo="REG"),
        Categoria(categoria="Bermuda", codigo="BER"),
        Categoria(categoria="Meia", codigo="MEI"),
        Categoria(categoria="Camisa", codigo="CAM"),
        Categoria(categoria="Bone", codigo="BON"),
    ]

    subcategorias = [
        Subcategoria(subcategoria="Jeans", codigo="JEA"),
        Subcategoria(subcategoria="Gola V", codigo="GOV"),
        Subcategoria(subcategoria="Gola Careca", codigo="GOC"),
        Subcategoria(subcategoria="Moletom", codigo="MOL"),
        Subcategoria(subcategoria="Esporte", codigo="ESP"),
        Subcategoria(subcategoria="Aba Reta", codigo="ARE"),
        Subcategoria(subcategoria="Social", codigo="SOC"),
        Subcategoria(subcategoria="Jeans", codigo="JEA"),
    ]

    Categoria.objects.bulk_create(categorias)
    Subcategoria.objects.bulk_create(subcategorias)

    Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
                              endereco="Avenida Brasil", pessoa_contato="Cleidson",
                              email="cleidson@renner.com"),

    cores = ["Azul", "Verde", "Cinza", "Amarelo", "Preto"]
    fornecedor = Fornecedor.objects.first()
    usuario = User.objects.first()
    todas_categorias = Categoria.objects.all()
    todas_subcategorias = Subcategoria.objects.all()

    # Cria 120 Produtos no backend
    for i in range(120):
        Produto.objects.create(
            descricao="",
            genero="unissex",
            categoria=todas_categorias[randint(1, len(categorias)-1)],
            subcategoria=todas_subcategorias[randint(1, len(subcategorias)-1)],
            tamanho="42",
            cor=cores[randint(0, (len(cores)-1))],
            min_pecas=1,
            alerta_min=3,
            total_pecas=3,
            preco_compra=randint(30, 120),
            preco_venda=randint(121, 150),
            motivo_alteracao_preco="Novo produto",
            criado_por=usuario,
            criado_em=usuario,
            fornecedor=fornecedor
        )
