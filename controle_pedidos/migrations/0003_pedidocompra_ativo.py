# Generated by Django 3.1.7 on 2021-04-04 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0002_auto_20210402_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocompra',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
