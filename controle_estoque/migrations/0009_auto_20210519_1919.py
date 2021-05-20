# Generated by Django 3.1.7 on 2021-05-19 22:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_estoque', '0008_regex_cnpj_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='em_compra',
            field=models.BooleanField(default=False, help_text='Para processo de compras'),
        ),
        migrations.AlterField(
            model_name='fornecedor',
            name='telefone',
            field=models.CharField(help_text='Preencha o campo apenas com números.', max_length=11, validators=[django.core.validators.RegexValidator('^\\d{10,11}$', message='Por favor, insira apenas os números do telefone.')]),
        ),
    ]
