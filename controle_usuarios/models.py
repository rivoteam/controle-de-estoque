from django.db import models
from django.contrib.auth.models import User

ESTADOS_CHOICES = (
    ('SP', 'SP'),
    ('RJ', 'RJ'),
    ('SC', 'SC'),
    ('MG', 'MG'),
    ('MS', 'MS'),
)


class CargoFuncionario(models.Model):
    class Meta:
        verbose_name = "Cargo do Funcionario"
        verbose_name_plural = "Cargos de Funcionarios"

    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Funcionario(models.Model):
    funcionario = models.OneToOneField(User, related_name="funcionario", on_delete=models.CASCADE)
    cargo_funcionario = models.ForeignKey(CargoFuncionario, related_name='cargo_funcionario', on_delete=models.CASCADE)
    estado = models.CharField(max_length=100, choices=ESTADOS_CHOICES)
    telefone = models.CharField(max_length=11)
    endereco = models.CharField(max_length=300)
    cpf = models.CharField(max_length=15)
    image = models.ImageField(upload_to='controle_usuarios/media/images', verbose_name="Imagem", null=True, blank=True)
    data_admissao = models.DateField('Admitido em', auto_now_add=True)
    data_demissao = models.DateField('Demitido em', auto_now_add=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.funcionario} - {self.cargo_funcionario}'

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['funcionario']
