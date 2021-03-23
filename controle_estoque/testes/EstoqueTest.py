from random import choice, randint
from django.contrib.auth.models import User
from django.test import TestCase
from controle_estoque.models import Produto, Subcategoria, Categoria, Fornecedor


class EstoqueTest(TestCase):
    """ Classe Base para os testes de Controle de Estoque """
    def setUp(self):
        # dicionário com chave=categoria e valor=codigo para criação da lista abaixo
        dic_categorias = {"Camiseta": "CAT", "Calca": "CAL", "Tenis": "TEN", "Blusa": "BLU", "Regata": "REG",
                          "Bermuda": "BER", "Meia": "MEI", "Camisa": "CAM", "Bone": "BON"}

        # dicionário com chave=subcategoria e valor=codigo para criação da lista abaixo
        dic_subcategorias = {"Jeans": "JEA", "Gola V": "GOV", "Gola Careca": "GOC", "Moletom": "MOL", "Esporte": "ESP",
                             "Aba Reta": "ARE", "Social": "SOC", "Soquete": "SOQ"}

        # Cria uma lista de objetos Categoria com o dic_categorias acima sem salvar no banco de dados
        categorias = [Categoria(categoria=k, codigo=v) for k, v in dic_categorias.items()]

        # Cria uma lista de objetos Subcategoria com o dic_subcategorias acima sem salvar no banco de dados
        subcategorias = [Subcategoria(subcategoria=k, codigo=v) for k, v in dic_subcategorias.items()]

        # Insere todas as categorias e subcategorias de uma vez no banco de dados
        Categoria.objects.bulk_create(categorias)
        Subcategoria.objects.bulk_create(subcategorias)

        # Cria um fornecedor no banco de dados
        self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
                                                    endereco="Avenida Brasil", pessoa_contato="Cleidson",
                                                    email="cleidson@renner.com")

        # Cria um usuário no banco de dados
        self.usuario = User.objects.create(username="admin", password="admin")

        # Variáveis para a criação do Produto
        self.cores = ["Azul", "Verde", "Cinza", "Amarelo", "Preto", "Branco"]
        self.generos = ["Masculino", "Feminino", "Unissex"]
        self.tamanhos = [str(ns) for ns in range(1, 6)] + [str(n) for n in range(30, 62, 2)] + ["P", "M", "G", "GG",
                                                                                                "XG"]

        # Queries para armazenar todas as categorias e subcategorias criadas acima
        self.todas_categorias = Categoria.objects.all()
        self.todas_subcategorias = Subcategoria.objects.all()

        # Cria 10 produtos no banco de dados
        for i in range(10):
            Produto.objects.create(
                descricao=f"Descrição do Produto 1",
                genero=choice(self.generos),
                categoria=self.todas_categorias[randint(1, len(self.todas_categorias) - 1)],
                subcategoria=self.todas_subcategorias[randint(1, len(self.todas_subcategorias) - 1)],
                tamanho=choice(self.tamanhos),
                cor=choice(self.cores),
                min_pecas=randint(0, 40),
                alerta_min=randint(41, 70),
                total_pecas=randint(0, 100),
                preco_compra=randint(20, 120),
                preco_venda=randint(121, 150),
                motivo_alteracao_preco="Novo produto",
                auto_pedido=choice([True, False]),
                criado_por=self.usuario,
                fornecedor=self.fornecedor
            )
        self.todos_produtos = Produto.objects.all()

        # Cria apenas um objeto Produto para ser utilizado nos testes
        self.categoria = Categoria.objects.get(categoria="Camiseta")
        self.subcategoria = Subcategoria.objects.get(subcategoria="Gola V")
        self.tamanho = "M"
        self.genero = "Masculino"
        self.novo_produto = Produto(
            descricao=f"Descrição do Novo Produto",
            genero=self.genero,
            categoria=self.categoria,
            subcategoria=self.subcategoria,
            tamanho=self.tamanho,
            cor="Azul",
            min_pecas=20,
            alerta_min=40,
            total_pecas=70,
            preco_compra=25,
            preco_venda=45,
            motivo_alteracao_preco="Novo produto",
            auto_pedido=True,
            criado_por=self.usuario,
            fornecedor=self.fornecedor
        )
