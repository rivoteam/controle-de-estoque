# Generated by Django 3.1.7 on 2021-04-02 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controle_estoque', '0002_auto_20210402_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
