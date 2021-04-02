# Generated by Django 3.1.7 on 2021-04-02 02:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('controle_estoque', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicoatualizacaoprecos',
            name='atualizado_por',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hist_atualizado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historicoatualizacaoprecos',
            name='criado_por',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='hist_preco_criado_por', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historicoatualizacaoprecos',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hist_preco_produto', to='controle_estoque.produto'),
        ),
    ]
