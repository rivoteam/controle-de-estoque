"""
Feito para testar em desenvolvimento e popular banco de dados
Instruções:
Executar o seguinte comando no terminal ou cmd:
python manage.py runscript run
"""

from django.contrib.auth.models import User
from random import randint, choice
from controle_estoque.models import Produto, Categoria, Subcategoria, Fornecedor
from controle_pedidos.models import PedidoCompra, CarrinhoPedido


def run():
    dic_categorias = {"Camiseta": "CAT", "Calca": "CAL", "Tenis": "TEN", "Blusa": "BLU", "Regata": "REG",
                      "Bermuda": "BER", "Meia": "MEI", "Camisa": "CAM", "Bone": "BON"}
    categorias = [Categoria(categoria=k, codigo=v) for k, v in dic_categorias.items()]

    dic_subcategorias = {"Jeans": "JEA", "Gola V": "GOV", "Gola Careca": "GOC", "Moletom": "MOL", "Esporte": "ESP",
                         "Aba Reta": "ARE", "Social": "SOC", "Soquete": "SOQ"}
    subcategorias = [Subcategoria(subcategoria=k, codigo=v) for k, v in dic_subcategorias.items()]

    Categoria.objects.bulk_create(categorias)
    Subcategoria.objects.bulk_create(subcategorias)

    Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
                              endereco="Avenida Brasil", pessoa_contato="Cleidson",
                              email="cleidson@renner.com"),

    cores = ["Azul", "Verde", "Cinza", "Amarelo", "Preto", "Branco"]
    generos = ["masculino", "feminino", "unissex"]
    tamanho = [str(ns) for ns in range(1, 6)] + [str(n) for n in range(30, 62, 2)] + ["P", "M", "G", "GG", "XG"]
    fornecedor = Fornecedor.objects.first()
    usuario = User.objects.first()
    todas_categorias = Categoria.objects.all()
    todas_subcategorias = Subcategoria.objects.all()

    for i in range(120):
        Produto.objects.create(
            descricao=f"Descrição do Produto {i + 1}",
            genero=choice(generos),
            categoria=todas_categorias[randint(1, len(categorias) - 1)],
            subcategoria=todas_subcategorias[randint(1, len(subcategorias) - 1)],
            tamanho=choice(tamanho),
            cor=choice(cores),
            min_pecas=randint(0, 40),
            alerta_min=randint(41, 70),
            total_pecas=randint(0, 100),
            preco_compra=randint(20, 120),
            preco_venda=randint(121, 150),
            motivo_alteracao_preco="Novo produto",
            auto_pedido=choice([True, False]),
            criado_por=usuario,
            fornecedor=fornecedor
        )

    for p in range(5):
        PedidoCompra.objects.create(fornecedor=fornecedor, descricao=f"Pedido {p + 1}", criado_por=usuario)

    todos_produtos = Produto.objects.all()
    todos_pedidos = PedidoCompra.objects.all()

    for p in range(40):
        CarrinhoPedido.objects.create(produto=choice(todos_produtos), quantidade=randint(1, 12),
                                      pedidocompra=choice(todos_pedidos))
