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
        return self.funcionario.groups.filter(name='gerente').exists()

    def is_analyst(self):
        return self.funcionario.groups.filter(name='analista').exists()

    def is_manager_or_cashier(self):
        return self.funcionario.groups.filter(name__in=['gerente', 'caixa']).exists()

    def is_manager_or_analyst(self):
        return self.funcionario.groups.filter(name__in=['gerente', 'analista']).exists()

    def is_manager_or_analyst_or_cashier(self):
        return self.funcionario.groups.filter(name__in=['gerente', 'analista', 'caixa']).exists()

    def is_manager_or_analyst_or_cashier_or_seller(self):
        return self.funcionario.groups.filter(name__in=['gerente', 'analista', 'caixa', 'vendedor']).exists()

    def is_manager_or_analyst_or_stockist(self):
        return self.funcionario.groups.filter(name__in=['gerente', 'analista', 'estoquista']).exists()

    def is_stockist(self):
        return self.funcionario.groups.filter(name='estoquista').exists()


    # //TODO Criar funções e incluir no CHOICES em utils.py
    '''
    def is_developer(self):
        return self.funcionario.groups.filter(name='desenvolvedor').exists()

    def is_admin(self):
        return self.funcionario.groups.filter(name='administrador').exists()
    '''
