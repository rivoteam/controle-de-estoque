# Generated by Django 3.1.7 on 2021-05-20 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_pedidos', '0006_auto_20210519_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocompra',
            name='csv_compra',
            field=models.FileField(blank=True, null=True, upload_to='pedidos_gerados/'),
        ),
    ]
