from controle_estoque.models import Fornecedor
from .EstoqueTest import EstoqueTest


class FornecedorTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_cria_novo_fornecedor(self):
        """ Deve criar um novo fornecedor """
        fornecedor = Fornecedor.objects.create(
            nome_empresa="Hering", cnpj="1019283745", telefone="111111",
            endereco="Avenida Paulista", pessoa_contato="Jadson",
            email="jadson@hering.com"
        )
        self.assertEqual(2, len(Fornecedor.objects.all()))
        self.assertTrue(Fornecedor.objects.filter(pk=fornecedor.pk).exists())
