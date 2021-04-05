# from django.contrib.auth.models import User
# from django.test import TestCase
#
# from controle_estoque.models import Produto, Categoria, Subcategoria, Fornecedor
# from controle_estoque.testes import EstoqueTest
# from interfaces.forms import EditaProdutoForm
#
#
# class EditaProdutoFormTest(TestCase):
#     def setUp(self):
#         self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
#                                                     endereco="Avenida Brasil", pessoa_contato="Cleidson",
#                                                     email="cleidson@renner.com")
#         self.usuario = User.objects.create(username="admin", password="admin")
#         self.categoria = Categoria.objects.create(categoria="Camiseta", codigo="CAT")
#         self.subcategoria = Subcategoria.objects.create(subcategoria="Gola V", codigo="GOV")
#         self.tamanho = "M"
#         self.genero = "Masculino"
#         self.novo_produto = Produto.objects.create(
#             descricao=f"Descrição do Novo Produto",
#             genero=self.genero,
#             categoria=self.categoria,
#             subcategoria=self.subcategoria,
#             tamanho=self.tamanho,
#             cor="Azul",
#             min_pecas=20,
#             alerta_min=40,
#             total_pecas=70,
#             preco_compra=25,
#             preco_venda=45,
#             motivo_alteracao_preco="Novo produto",
#             auto_pedido=True,
#             criado_por=self.usuario,
#             fornecedor=self.fornecedor
#         )
#         self.response = self.client.get(f'/edita-produto/{self.novo_produto.pk}')
#
#     def test_get(self):
#         self.novo_produto.save()
#         self.assertEqual(200, self.response.status_code)
#
#     def test_template_usado(self):
#         self.assertTemplateUsed(self.response, 'modal_edita_produto.html')
#
#     def test_html(self):
#         expected = [('<form', 1), ('<input', 9), ('type="text"', 3), ('type="number"', 5),
#                     ('<select', 5), ('<i class=', 1), ('type="button"', 1), ('type="submit"', 2)]
#         for text, count in expected:
#             with self.subTest():
#                 self.assertContains(self.response, text, count)
#
#     def test_csrf(self):
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_formulario_existe(self):
#         form = self.response.context['form']
#         self.assertIsInstance(form, EditaProdutoForm)
#
#     def test_form_fields(self):
#         form = EditaProdutoForm()
#         expected = ['descricao', 'genero', 'categoria', 'subcategoria', 'tamanho', 'cor', 'min_pecas', 'alerta_min',
#                     'total_pecas', 'preco_compra', 'preco_venda', 'motivo_alteracao_preco', 'auto_pedido', 'fornecedor']
#         self.assertSequenceEqual(expected, list(form.fields))
#
#
# class EditaProdutoPostValidoTest(TestCase):
#     def setUp(self):
#         self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
#                                                     endereco="Avenida Brasil", pessoa_contato="Cleidson",
#                                                     email="cleidson@renner.com")
#         self.usuario = User.objects.create(username="admin", password="admin")
#         self.categoria = Categoria.objects.create(categoria="Camiseta", codigo="CAT")
#         self.subcategoria = Subcategoria.objects.create(subcategoria="Gola V", codigo="GOV")
#         self.tamanho = "M"
#         self.genero = "Masculino"
#         self.novo_produto = Produto.objects.create(
#             descricao=f"Descrição do Novo Produto",
#             genero=self.genero,
#             categoria=self.categoria,
#             subcategoria=self.subcategoria,
#             tamanho=self.tamanho,
#             cor="Azul",
#             min_pecas=20,
#             alerta_min=40,
#             total_pecas=70,
#             preco_compra=25,
#             preco_venda=45,
#             motivo_alteracao_preco="Novo produto",
#             auto_pedido=True,
#             criado_por=self.usuario,
#             fornecedor=self.fornecedor
#         )
#         self.response = self.client.post(f'/edita-produto/{self.novo_produto.pk}')
#
#     def test_post(self):
#         self.assertEqual(302, self.response.status_code)
#
#     def test_form_errors(self):
#         form = self.response.context['form']
#         self.assertFalse(form.errors)
#
#
# class EditaProdutoPostInvalidoTest(TestCase):
#     def setUp(self):
#         self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
#                                                     endereco="Avenida Brasil", pessoa_contato="Cleidson",
#                                                     email="cleidson@renner.com")
#         self.usuario = User.objects.create(username="admin", password="admin")
#         self.categoria = Categoria.objects.create(categoria="Camiseta", codigo="CAT")
#         self.subcategoria = Subcategoria.objects.create(subcategoria="Gola V", codigo="GOV")
#         self.tamanho = "M"
#         self.genero = "Masculino"
#         self.novo_produto = Produto.objects.create(
#             descricao=f"Descrição do Novo Produto",
#             genero=self.genero,
#             categoria=self.categoria,
#             subcategoria=self.subcategoria,
#             tamanho=self.tamanho,
#             cor="Azul",
#             min_pecas=20,
#             alerta_min=40,
#             total_pecas=70,
#             preco_compra=25,
#             preco_venda=45,
#             motivo_alteracao_preco="Novo produto",
#             auto_pedido=True,
#             criado_por=self.usuario,
#             fornecedor=self.fornecedor
#         )
#         self.response = self.client.post(f'/edita-produto/{self.novo_produto.pk}')
#
#     def test_post(self):
#         self.assertEqual(200, self.response.status_code)
#
#     def test_template_usado(self):
#         self.assertTemplateUsed(self.response, 'modal_edita_produto.html')
#
#     def test_formulario_existe(self):
#         form = self.response.context['form']
#         self.assertIsInstance(form, EditaProdutoForm)
#
#     def test_form_errors(self):
#         form = self.response.context['form']
#         self.assertTrue(form.errors)
#
# '''
# class EditaProdutoMensagemSucesso(TestCase):
#     def setUp(self):
#         self.fornecedor = Fornecedor.objects.create(nome_empresa="Renner", cnpj="123216351", telefone="00000",
#                                                     endereco="Avenida Brasil", pessoa_contato="Cleidson",
#                                                     email="cleidson@renner.com")
#         self.usuario = User.objects.create(username="admin", password="admin")
#         self.categoria = Categoria.objects.create(categoria="Camiseta", codigo="CAT")
#         self.subcategoria = Subcategoria.objects.create(subcategoria="Gola V", codigo="GOV")
#         self.tamanho = "M"
#         self.genero = "Masculino"
#         self.novo_produto = Produto.objects.create(
#             descricao=f"Descrição do Novo Produto",
#             genero=self.genero,
#             categoria=self.categoria,
#             subcategoria=self.subcategoria,
#             tamanho=self.tamanho,
#             cor="Azul",
#             min_pecas=20,
#             alerta_min=40,
#             total_pecas=70,
#             preco_compra=25,
#             preco_venda=45,
#             motivo_alteracao_preco="Novo produto",
#             auto_pedido=True,
#             criado_por=self.usuario,
#             fornecedor=self.fornecedor
#         )
#         self.response = self.client.post(f'/edita-produto/{self.novo_produto.pk}')
#
#     def test_mensagem(self):
#         # data = {'descricao': 'Descrição do Produto', 'genero': 'Masculino', 'categoria': 1,
#         #         'subcategoria': 2, 'tamanho': 'G', 'cor': 'Branca', 'min_pecas': 10, 'alerta_min': 20,
#         #         'total_pecas': 37, 'preco_compra': 25.00, 'preco_venda': 35.00,
#         #         'motivo_alteracao_preco': 'Produto Novo', 'auto_pedido': True, 'fornecedor': 1}
#         # form = EditaProdutoForm(data)
#         # form = EditaProdutoForm(instance=self.novo_produto)
#         response = self.client.post(f'/edita-produto/{self.novo_produto.pk}', follow=True)
#         self.assertContains(response, "Produto atualizado com sucesso!")
# '''