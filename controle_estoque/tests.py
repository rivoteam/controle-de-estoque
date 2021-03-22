from random import choice, randint
from django.contrib.auth.models import User
from django.test import TestCase
from controle_estoque.models import Produto, Subcategoria, Categoria, Fornecedor, HistoricoAtualizacaoPrecos
from core.signals import generate_barcode


class EstoqueTest(TestCase):
    def setUp(self):
        dic_categorias = {"Camiseta": "CAT", "Calca": "CAL", "Tenis": "TEN", "Blusa": "BLU", "Regata": "REG",
                          "Bermuda": "BER", "Meia": "MEI", "Camisa": "CAM", "Bone": "BON"}
        categorias = [Categoria(categoria=k, codigo=v) for k, v in dic_categorias.items()]

        dic_subcategorias = {"Jeans": "JEA", "Gola V": "GOV", "Gola Careca": "GOC", "Moletom": "MOL", "Esporte": "ESP",
                             "Aba Reta": "ARE", "Social": "SOC", "Soquete": "SOQ"}
        subcategorias = [Subcategoria(subcategoria=k, codigo=v) for k, v in dic_subcategorias.items()]

        Categoria.objects.bulk_create(categorias)
        Subcategoria.objects.bulk_create(subcategorias)

        self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
                                                    endereco="Avenida Brasil", pessoa_contato="Cleidson",
                                                    email="cleidson@renner.com")

        self.usuario = User.objects.create(username="admin", password="admin")

        self.cores = ["Azul", "Verde", "Cinza", "Amarelo", "Preto", "Branco"]
        self.generos = ["Masculino", "Feminino", "Unissex"]
        self.tamanhos = [str(ns) for ns in range(1, 6)] + [str(n) for n in range(30, 62, 2)] + ["P", "M", "G", "GG",
                                                                                                "XG"]
        self.todas_categorias = Categoria.objects.all()
        self.todas_subcategorias = Subcategoria.objects.all()

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

        # Para criação de um produto nos testes abaixo
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

    def test_len_Categoria(self):
        self.assertEqual(9, len(self.todas_categorias))

    def test_create_category(self):
        new_category = Categoria.objects.create(categoria="blAZer", codigo="blA")
        self.assertEqual(len(self.todas_categorias) + 1, len(Categoria.objects.all()))
        self.assertEqual("Blazer", new_category.categoria)
        self.assertEqual("BLA", new_category.codigo)

    def test_len_Subcategoria(self):
        self.assertEqual(8, len(self.todas_subcategorias))

    def test_create_subcategory(self):
        new_subcategory = Subcategoria.objects.create(subcategoria="espORte FinO", codigo="eSf")
        self.assertEqual(len(self.todas_subcategorias) + 1, len(Subcategoria.objects.all()))
        self.assertEqual("Esporte Fino", new_subcategory.subcategoria)
        self.assertEqual("ESF", new_subcategory.codigo)

    def test_len_Fornecedor(self):
        self.assertEqual(1, len(Fornecedor.objects.all()))

    def test_name_Fornecedor(self):
        fornecedor = Fornecedor.objects.first()
        self.assertEqual("Renner", fornecedor.nome_empresa)

    def test_len_User(self):
        self.assertEqual(1, len(User.objects.all()))

    def test_name_usuario_criado(self):
        self.assertEqual("admin", User.objects.first().username)

    def test_len_Produto(self):
        self.assertEqual(10, len(Produto.objects.all()))

    def test_generate_unique_barcode(self):
        for i in range(10):
            choice_produto = choice(self.todos_produtos)
            ean_one_product = choice_produto.ean
            barcode = generate_barcode(ean_one_product)
            with self.subTest():
                self.assertNotEqual(ean_one_product, barcode)
                self.assertEqual(0, len(Produto.objects.filter(ean=barcode)))

    def test_generate_sku(self):
        for produto in self.todos_produtos:
            genero = produto.genero[:1]
            codigo_categoria = produto.categoria.codigo
            codigo_subcategoria = produto.subcategoria.codigo
            tamanho_sku = f"{(2 - len(produto.tamanho)) * '0'}{produto.tamanho}"
            with self.subTest():
                self.assertEqual(produto.sku, f"{genero}{codigo_categoria}{codigo_subcategoria}{tamanho_sku}")

    def test_sku_creating_product(self):
        self.novo_produto.save()
        self.assertEqual("MCATGOV0M", self.novo_produto.sku)

    def test_create_product(self):
        self.novo_produto.save()
        historico = HistoricoAtualizacaoPrecos.objects.get(produto=self.novo_produto)
        self.assertEqual(None, self.novo_produto.motivo_alteracao_preco)
        self.assertEqual("Novo produto", historico.motivo_alteracao_preco)

    def test_update_product_price(self):
        self.novo_produto.save()
        self.novo_produto.preco_venda += 10.00
        self.novo_produto.motivo_alteracao_preco = "Reajuste"
        self.novo_produto.save()
        historico = HistoricoAtualizacaoPrecos.objects.filter(produto=self.novo_produto).first()
        self.assertEqual(None, self.novo_produto.motivo_alteracao_preco)
        self.assertEqual("Reajuste", historico.motivo_alteracao_preco)
