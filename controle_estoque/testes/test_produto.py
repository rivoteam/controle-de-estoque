from django.db.utils import IntegrityError
from controle_estoque.models import Produto, HistoricoAtualizacaoPrecos
from .EstoqueTest import EstoqueTest


class ProdutoTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_cria_novo_produto(self):
        """ Deve criar um novo produto com os dados do setUp() """
        self.novo_produto.save()
        produto_salvo = Produto.objects.get(ean=self.novo_produto.ean)
        historico = HistoricoAtualizacaoPrecos.objects.filter(produto=produto_salvo).first()
        self.assertIsNone(produto_salvo.motivo_alteracao_preco)
        self.assertEqual("Novo produto", historico.motivo_alteracao_preco)

    def test_atualiza_preco_do_produto(self):
        """ Deve atualizar o preço do produto com o motivo_alteracao_preco=None e criar um novo registro na tabela
        HistoricoAtualizacaoPrecos com motivo_alteracao_preco=Reajuste """
        self.novo_produto.save()
        produto_salvo = Produto.objects.get(ean=self.novo_produto.ean)
        produto_salvo.preco_venda += 10
        produto_salvo.motivo_alteracao_preco = "Reajuste"
        produto_salvo.save()
        produto_alterado = Produto.objects.get(ean=self.novo_produto.ean)
        historico = HistoricoAtualizacaoPrecos.objects.filter(produto=produto_alterado).first()
        self.assertIsNone(produto_alterado.motivo_alteracao_preco)
        self.assertEqual("Reajuste", historico.motivo_alteracao_preco)


class ProdutoTestesDadosInValidos(EstoqueTest):
    """ Testes com dados inválidos informados """
    def test_cria_novo_produto_sem_preco_venda(self):
        """ Não deve criar um novo produto com os dados do setUp() """
        with self.assertRaises((IntegrityError, TypeError)):
            self.novo_produto.genero = None
            self.novo_produto.save()

    def test_cria_novo_produto_sem_criado_por(self):
        """ Não deve criar um novo produto com os dados do setUp() """
        with self.assertRaises(IntegrityError):
            self.novo_produto.criado_por = None
            self.novo_produto.save()
