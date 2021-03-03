# Generated by Django 3.1.7 on 2021-03-03 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterField(
            model_name='pedido',
            name='preco_pedido',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Preço Total do Pedido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Gerado'), (2, 'Em separação'), (3, 'Enviado'), (4, 'Concluído')], default=1, verbose_name='Status'),
        ),
    ]
