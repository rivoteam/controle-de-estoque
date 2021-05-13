from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

from core.utils import CARGOS_CHOICES


class Funcionario(models.Model):
    funcionario = models.OneToOneField(User, related_name="funcionario", on_delete=models.CASCADE)
    cargo_funcionario = models.CharField(choices=CARGOS_CHOICES, max_length=255)
    telefone = models.CharField(max_length=11, help_text='Preencha o campo apenas com números.', validators=[
        RegexValidator(r'^\d{10,11}$', message='Por favor, insira apenas os números do telefone.')])
    cpf = models.CharField('CPF', max_length=11, help_text='Preencha o campo apenas com números.', validators=[
        RegexValidator(r'^\d{11,11}$', message='Por favor, não insira letras, " . " e " - " no campo abaixo.')])
    endereco = models.CharField(max_length=300)
    image = models.ImageField(upload_to='controle_usuarios/media/images', default='static/img/theme/avocado.png',
                              verbose_name="Imagem", null=True, blank=True)
    data_admissao = models.DateField('Admitido em', auto_now_add=True)
    data_demissao = models.DateField('Demitido em', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.funcionario.first_name} {self.funcionario.last_name}'

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['funcionario']

    def is_manager(self):
        if self.cargo_funcionario == "gerente":
            return True
