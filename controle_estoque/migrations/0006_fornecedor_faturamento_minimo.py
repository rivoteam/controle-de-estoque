# Generated by Django 3.1.7 on 2021-04-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_estoque', '0005_auto_20210409_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='faturamento_minimo',
            field=models.IntegerField(default=1000),
        ),
    ]
