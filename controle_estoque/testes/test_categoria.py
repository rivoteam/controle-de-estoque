from controle_estoque.models import Categoria
from .EstoqueTest import EstoqueTest


class CategoriaTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_cria_nova_categoria(self):
        """ Deve criar uma nova categoria """
        nova_categoria = Categoria.objects.create(categoria="Blazer", codigo="BLA")
        self.assertEqual(len(self.todas_categorias) + 1, len(Categoria.objects.all()))
        self.assertTrue(Categoria.objects.filter(pk=nova_categoria.pk).exists())

    def test_categoria_salvo_com_maiuscula(self):
        """ Deve criar a categoria com a primeira letra de cada palavra em maiúscula """
        nova_categoria = Categoria.objects.create(categoria="blAZer", codigo="blA")
        self.assertEqual("Blazer", nova_categoria.categoria)

    def test_codigo_salvo_com_maiusculo(self):
        """ Deve criar o código para categoria com todas as letras em maiúscula """
        nova_categoria = Categoria.objects.create(categoria="blAZer", codigo="blA")
        self.assertEqual("BLA", nova_categoria.codigo)


class CategoriaTestesDadosInvalidos(EstoqueTest):
    """ Testes com dados inválidos informados """
    def test_cria_nova_categoria(self):
        """ Não deve criar uma nova categoria sem código """
        nova_categoria = Categoria.objects.create(categoria="Blazer")
        self.assertEqual(len(self.todas_categorias) + 1, len(Categoria.objects.all()))
        self.assertTrue(Categoria.objects.filter(pk=nova_categoria.pk).exists())