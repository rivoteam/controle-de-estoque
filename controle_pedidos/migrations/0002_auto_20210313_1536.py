# Generated by Django 3.1.7 on 2021-03-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedidocompra',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'Gerado'), (2, 'Em separação'), (3, 'Enviado'), (4, 'Mecadoria Recebida'), (5, 'Concluído')], default=1, verbose_name='Status'),
        ),
    ]
