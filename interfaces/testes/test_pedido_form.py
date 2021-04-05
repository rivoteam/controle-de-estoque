from django.test import TestCase

from controle_estoque.models import Fornecedor
from interfaces.forms import PedidoForm


class PedidoFormTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/cria-pedido')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'cria-pedido.html')

    def test_html(self):
        tags = (
            ('<form', 1),
            ('<textarea', 1),
            ('type="submit', 1),
            ('type="file', 1),
            ('<select', 2),
            ('<table', 1),
            ('<th>', 5),
        )
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, PedidoForm)


class PedidoFormPostValid(TestCase):
    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
                                  endereco="Avenida Brasil", pessoa_contato="Cleidson",
                                  email="cleidson@renner.com")
        data = {
            # 'status': 1,
            'fornecedor': 1,
            'descricao': 'Descrição do Pedido'
        }
        self.response = self.client.post('/cria-pedido', data)

    def test_post(self):
        self.assertRedirects(self.response, 'lista-pedidos')
