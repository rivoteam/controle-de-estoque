# Generated by Django 3.1.7 on 2021-02-19 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CargoFuncionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cargo do Funcionario',
                'verbose_name_plural': 'Cargos de Funcionarios',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('SP', 'SP'), ('RJ', 'RJ'), ('SC', 'SC'), ('MG', 'MG'), ('MS', 'MS')], max_length=100)),
                ('telefone', models.CharField(max_length=11)),
                ('endereco', models.CharField(max_length=300)),
                ('cpf', models.CharField(max_length=15)),
                ('image', models.ImageField(blank=True, null=True, upload_to='controle_usuarios/media/images', verbose_name='Imagem')),
                ('data_admissao', models.DateField(auto_now_add=True, verbose_name='Admitido em')),
                ('data_demissao', models.DateField(auto_now_add=True, verbose_name='Demitido em')),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('cargo_funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cargo_funcionario', to='controle_usuarios.cargofuncionario')),
                ('funcionario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'ordering': ['funcionario'],
            },
        ),
    ]
