from controle_estoque.models import Subcategoria, Categoria
from .EstoqueTest import EstoqueTest


class SubcategoriaTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_cria_nova_subcategoria(self):
        """ Deve criar uma nova subcategoria """
        nova_subcategoria = Subcategoria.objects.create(subcategoria="Esporte Fino", codigo="ESF")
        self.assertEqual(len(self.todas_subcategorias) + 1, len(Subcategoria.objects.all()))
        self.assertTrue(Subcategoria.objects.filter(pk=nova_subcategoria.pk).exists())

    def test_subcategoria_salvo_com_maiuscula(self):
        """ Deve criar a subcategoria com a primeira letra de cada palavra em maiúscula """
        nova_subcategoria = Subcategoria.objects.create(subcategoria="espORte FinO", codigo="eSf")
        self.assertEqual("Esporte Fino", nova_subcategoria.subcategoria)

    def test_codigo_salvo_com_maiusculo(self):
        """ Deve criar o código para subcategoria com todas as letras em maiúscula """
        nova_subcategoria = Categoria.objects.create(categoria="espORte FinO", codigo="eSf")
        self.assertEqual("ESF", nova_subcategoria.codigo)
