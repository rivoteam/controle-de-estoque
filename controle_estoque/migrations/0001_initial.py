# Generated by Django 3.1.7 on 2021-03-03 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=30)),
                ('codigo', models.CharField(max_length=3)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categoria_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='categoria_criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['categoria'],
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_empresa', models.CharField(max_length=150)),
                ('cnpj', models.CharField(max_length=15)),
                ('telefone', models.CharField(max_length=11)),
                ('endereco', models.CharField(max_length=300)),
                ('pessoa_contato', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=120)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('SP', 'SP'), ('RJ', 'RJ'), ('SC', 'SC'), ('MG', 'MG'), ('MS', 'MS')], default='SP', max_length=100)),
                ('ativo', models.BooleanField(default=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='fornecedor_criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome_empresa'],
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.CharField(max_length=15)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='genero_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='genero_criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
                'ordering': ['genero'],
            },
        ),
        migrations.CreateModel(
            name='TamanhoProduto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamanho', models.CharField(max_length=2)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tamanho_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='tamanho_criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tamanho do Produto',
                'verbose_name_plural': 'Tamanho dos Produtos',
                'ordering': ['tamanho'],
            },
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategoria', models.CharField(max_length=30)),
                ('codigo', models.CharField(max_length=3)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategoria_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='subcategoria_criado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subcategoria',
                'verbose_name_plural': 'Subcategorias',
                'ordering': ['subcategoria'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50)),
                ('cor', models.CharField(max_length=30)),
                ('grade', models.CharField(max_length=30)),
                ('min_pecas', models.PositiveSmallIntegerField()),
                ('alerta_min', models.PositiveSmallIntegerField()),
                ('limite_alerta_min', models.BooleanField(default=False, editable=False)),
                ('total_pecas', models.PositiveSmallIntegerField()),
                ('preco_compra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preco_venda', models.DecimalField(decimal_places=2, max_digits=6)),
                ('motivo_alteracao_preco', models.CharField(default='Novo produto', max_length=300, null=True)),
                ('auto_pedido', models.BooleanField(default=False)),
                ('ean', models.CharField(editable=False, max_length=13)),
                ('sku', models.CharField(editable=False, max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produto_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_estoque.categoria')),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='produto_criado_por', to=settings.AUTH_USER_MODEL)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_estoque.fornecedor')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_estoque.genero')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_estoque.subcategoria')),
                ('tamanho', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='controle_estoque.tamanhoproduto')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['descricao'],
            },
        ),
    ]
