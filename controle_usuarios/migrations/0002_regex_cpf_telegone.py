# Generated by Django 3.1.7 on 2021-05-13 13:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='cpf',
            field=models.CharField(help_text='Preencha o campo apenas com números.', max_length=11, validators=[django.core.validators.RegexValidator('^\\d{11,11}$', message='Por favor, não insira letras, " . " e " - " no campo abaixo.')], verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='telefone',
            field=models.CharField(help_text='Preencha o campo sem " ( ) " do DDD.', max_length=11, validators=[django.core.validators.RegexValidator('^\\d{10,11}$', message='Por favor, insira apenas os números do telefone.')]),
        ),
    ]
