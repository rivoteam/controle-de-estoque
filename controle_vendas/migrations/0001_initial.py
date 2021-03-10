# Generated by Django 3.1.7 on 2021-03-10 00:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('controle_estoque', '0001_initial'),
        ('controle_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, max_length=150, null=True, verbose_name='Descrição da Venda')),
                ('status', models.SmallIntegerField(choices=[(1, 'Pendente'), (2, 'Cancelada'), (3, 'Concluída')], default=1, verbose_name='Status')),
                ('nota_fiscal', models.FileField(blank=True, null=True, upload_to='controle_pedidos/NFE', verbose_name='Nota Fiscal Eletronica')),
                ('cpf', models.CharField(blank=True, max_length=30, null=True, verbose_name='CPF')),
                ('desconto', models.DecimalField(decimal_places=2, default=0, help_text='Digite o valor de desconto da venda, exemplo R$ 10,00', max_digits=12, verbose_name='Desconto')),
                ('forma_pagto', models.SmallIntegerField(choices=[(1, 'Debito'), (2, 'Credito'), (3, 'Dinheiro'), (4, 'PicPay'), (5, 'Pix')], verbose_name='Forma De Pagamento')),
                ('valor_total_venda', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Valor Total da Venda')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Venda Realizada Em')),
                ('caixa', models.ForeignKey(help_text='Caixa que está efetuando a venda', on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendas_caixa', to='controle_usuarios.funcionario', verbose_name='Operador/Caixa')),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendas_criadopor', to=settings.AUTH_USER_MODEL)),
                ('vendedor', models.ForeignKey(help_text='Vendedor que atendeu o cliente', on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendas_vendedor', to='controle_usuarios.funcionario', verbose_name='Vendedor')),
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
                ('status', models.SmallIntegerField(choices=[(1, 'Pendente'), (2, 'Cancelada'), (3, 'Concluída')], default='Concluída')),
                ('valor_total_diario', models.DecimalField(decimal_places=2, max_digits=6)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('caixa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='historico_caixa', to='controle_usuarios.funcionario')),
                ('criado_por', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='historico_criado', to=settings.AUTH_USER_MODEL)),
                ('vendas', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_vendas.venda')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='historico_vendedor', to='controle_usuarios.funcionario')),
            ],
            options={
                'verbose_name': 'Histórico de Venda',
                'verbose_name_plural': 'Histórico de Vendas',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='CarrinhoVenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_estoque.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='controle_vendas.venda')),
            ],
        ),
    ]
