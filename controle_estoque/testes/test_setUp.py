from random import choice
from django.contrib.auth.models import User
from controle_estoque.models import Produto, Fornecedor
from core.signals import generate_barcode
from .EstoqueTest import EstoqueTest


class SetUpTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_quantidade_de_categorias_criadas(self):
        """ Verifica se foram criadas 9 categorias no setUp() """
        self.assertEqual(9, len(self.todas_categorias))

    def test_quantidade_de_subcategorias_criadas(self):
        """ Verifica se foram criadas 9 subcategorias no setUp() """
        self.assertEqual(8, len(self.todas_subcategorias))

    def test_quantidade_fornecedores_criados(self):
        """ Verifica se foi criado 1 fornecedor no setUp() """
        self.assertEqual(1, len(Fornecedor.objects.all()))

    def test_nome_Fornecedor(self):
        """ Verifica o nome do fornecedor criado no setUp() """
        fornecedor = Fornecedor.objects.first()
        self.assertEqual("Renner", fornecedor.nome_empresa)

    def test_quantidade_de_usuarios_criados(self):
        """ Verifica se foi criado um usuário no setUp() """
        self.assertEqual(1, len(User.objects.all()))

    def test_nome_usuario_criado(self):
        """ Verifica o nome do usuário criado no setUp() """
        self.assertEqual("admin", User.objects.first().username)

    def test_quantidade_de_produtos_criados(self):
        """ Verifica a quantidade de produtos criados no setUp() """
        self.assertEqual(10, len(Produto.objects.all()))

    def test_gera_unico_codigo_de_barras(self):
        """ Deve criar um código de barras exclusivo para cada produto, sem repetir no banco de dados """
        for i in range(10):
            choice_produto = choice(self.todos_produtos)
            ean_one_product = choice_produto.ean
            barcode = generate_barcode(ean_one_product)
            with self.subTest():
                self.assertNotEqual(ean_one_product, barcode)
                self.assertEqual(0, len(Produto.objects.filter(ean=barcode)))

    def test_gera_codigo_sku(self):
        """ Verifica o sku de todos os produtos criados no setUp()
            Deve criar um código alfanumérico para SKU contendo: 123456789 => GCOCCOSTM
            G   = Dígito  1:        Primeira letra do gênero
            COC = Dígitos 2,3,4:    Código da categoria
            COS = Dígitos 5,6,7:    Código da subcategoria
            TM  = Dígitos 8,9:      Tamanho do produto. Se for um caractere acrescenta 0 antes, ex.: M = 0M
        """
        for produto in self.todos_produtos:
            genero = produto.genero[:1]
            codigo_categoria = produto.categoria.codigo
            codigo_subcategoria = produto.subcategoria.codigo
            tamanho_sku = f"{(2 - len(produto.tamanho)) * '0'}{produto.tamanho}"
            with self.subTest():
                self.assertEqual(produto.sku, f"{genero}{codigo_categoria}{codigo_subcategoria}{tamanho_sku}")