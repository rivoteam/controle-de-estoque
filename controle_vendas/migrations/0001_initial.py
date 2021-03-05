# Generated by Django 3.1.7 on 2021-03-05 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('controle_usuarios', '0001_initial'),
        ('controle_estoque', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='controle_estoque.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_total_venda', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Valor Total da Venda')),
                ('descricao', models.TextField(blank=True, max_length=150, null=True, verbose_name='Descrição da Venda')),
                ('nota_fiscal', models.FileField(blank=True, null=True, upload_to='controle_pedidos/NFE', verbose_name='Nota Fiscal Eletronica')),
                ('data_venda', models.DateTimeField(auto_now_add=True, verbose_name='Venda Realizada Em')),
                ('status', models.SmallIntegerField(choices=[(1, 'Gerado'), (2, 'Em separação'), (3, 'Enviado'), (4, 'Concluído')], default=1, verbose_name='Status')),
                ('forma_pagto', models.CharField(max_length=30, verbose_name='Forma De Pagamento')),
                ('cpf', models.CharField(max_length=30, verbose_name='CPF')),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caixa', to='controle_usuarios.funcionario')),
                ('criado_por', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('produtos', models.ManyToManyField(to='controle_vendas.VendaItem')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendedor', to='controle_usuarios.funcionario')),
            ],
            options={
                'verbose_name': 'Venda',
                'verbose_name_plural': 'Vendas',
            },
        ),
        migrations.CreateModel(
            name='HistoricoVendas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itens_compra', models.JSONField(default=dict)),
                ('status', models.CharField(choices=[('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')], default='Concluída', max_length=30)),
                ('valor_compra', models.DecimalField(decimal_places=2, max_digits=6)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargo_caixa', to='controle_usuarios.funcionario')),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hist_vendas_criado_por', to=settings.AUTH_USER_MODEL)),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargo_vendedor', to='controle_usuarios.funcionario')),
            ],
            options={
                'verbose_name': 'Histórico de Venda',
                'verbose_name_plural': 'Histórico de Vendas',
                'ordering': ['-criado_em'],
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
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hist_atual_preco_criado_por', to=settings.AUTH_USER_MODEL)),
                ('ean', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hist_atual_preco_produto', to='controle_estoque.produto')),
            ],
            options={
                'verbose_name': 'Historico de Atualização de Preços',
                'verbose_name_plural': 'Historico de Atualização de Preços',
                'ordering': ['-criado_em'],
            },
        ),
    ]
