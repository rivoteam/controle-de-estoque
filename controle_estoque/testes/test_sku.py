from .EstoqueTest import EstoqueTest


class SKUTestesDadosValidos(EstoqueTest):
    """ Testes com dados válidos informados """
    def test_gera_um_sku(self):
        """ Deve criar o código SKU da forma esperada """
        self.novo_produto.save()
        self.assertEqual("MCATGOV0M", self.novo_produto.sku)