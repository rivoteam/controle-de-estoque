# Generated by Django 3.1.7 on 2021-03-20 01:55

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
                ('categoria', models.CharField(max_length=30, unique=True)),
                ('codigo', models.CharField(max_length=3, unique=True)),
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
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome_empresa'],
            },
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategoria', models.CharField(max_length=30)),
                ('codigo', models.CharField(max_length=3)),
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
                ('genero', models.CharField(choices=[('masculino', 'Masculino'), ('feminino', 'Feminino'), ('unissex', 'Unissex')], max_length=255)),
                ('tamanho', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('30', '30'), ('32', '32'), ('34', '34'), ('36', '36'), ('38', '38'), ('40', '40'), ('42', '42'), ('44', '44'), ('46', '46'), ('48', '48'), ('50', '50'), ('52', '52'), ('54', '54'), ('56', '56'), ('58', '58'), ('60', '60'), ('P', 'P'), ('M', 'M'), ('G', 'G'), ('GG', 'GG'), ('XG', 'XG')], max_length=5, verbose_name='Tamanho')),
                ('cor', models.CharField(max_length=30)),
                ('min_pecas', models.PositiveSmallIntegerField()),
                ('alerta_min', models.PositiveSmallIntegerField()),
                ('limite_alerta_min', models.BooleanField(default=False, editable=False)),
                ('total_pecas', models.PositiveSmallIntegerField()),
                ('preco_compra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preco_venda', models.DecimalField(decimal_places=2, max_digits=6)),
                ('motivo_alteracao_preco', models.CharField(max_length=300, null=True)),
                ('auto_pedido', models.BooleanField(default=False)),
                ('ean', models.CharField(editable=False, max_length=13)),
                ('sku', models.CharField(editable=False, max_length=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_estoque.categoria')),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='produto_criado_por', to=settings.AUTH_USER_MODEL)),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_estoque.fornecedor')),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_estoque.subcategoria')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='HistoricoAtualizacaoPrecos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
                ('preco_compra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preco_venda', models.DecimalField(decimal_places=2, max_digits=6)),
                ('motivo_alteracao_preco', models.CharField(max_length=300)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('atualizado_por', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hist_atualizado_por', to=settings.AUTH_USER_MODEL)),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='hist_preco_criado_por', to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='hist_preco_produto', to='controle_estoque.produto')),
            ],
            options={
                'verbose_name': 'Historico de Atualização de Preços',
                'verbose_name_plural': 'Historico de Atualização de Preços',
                'ordering': ['-criado_em'],
            },
        ),
    ]
