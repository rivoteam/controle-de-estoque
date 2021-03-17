from django.http import HttpResponse
from django.conf import settings
from django.core import mail
from datetime import datetime
from core.settings import STATIC_URL
import csv
import xlwt
import logging


# logger = logging.getLogger('file')
logger = logging.getLogger(__name__)
# logger_db = logging.getLogger('django.db.backends')


GENERO_CHOICES = (
    ('masculino', "Masculino"),
    ('feminino', "Feminino"),
    ('unissex', "Unissex"),
)

STATUS_COMPRA_CHOICES = (
    (1, 'Gerado'),
    (2, 'Em separação'),
    (3, 'Enviado'),
    (4, 'Mecadoria Recebida'),
    (5, 'Concluído'),
)

CARGOS_CHOICES = (
    ("estoquista", "Estoquista"),
    ("caixa", "Caixa"),
    ("vendedor", "Vendedor"),
    ("analista", "Analista"),
    ("gerente", "Gerente"),
)

STATUS_VENDA_CHOICES = (
    (1, 'Pendente'),
    (2, 'Cancelada'),
    (3, 'Concluída'),
)

PAGAMENTO_CHOICES = (
    (1, 'Debito'),
    (2, 'Credito'),
    (3, 'Dinheiro'),
    (4, 'PicPay'),
    (5, 'Pix'),
)

numeros_social = tuple((str(n), str(n)) for n in range(1, 6))
numeros = tuple((str(n), str(n)) for n in range(30, 62, 2))
letras = tuple((l, l) for l in ["P", "M", "G", "GG", "XG"])
TAMANHO_CHOICES = numeros_social + numeros + letras


def get_user_profile(request):
    """
    Pega informações de usuario para renderizar foto de perfil e exibir nome nas paginas do site
    """
    context = {
        'profile_photo': STATIC_URL + 'img/theme/avocado.png',
        'fullname': f'{request.user.first_name} {request.user.last_name}',
    }
    if request.user.first_name == "":
        context['fullname'] = request.user.username
    if request.user.funcionario.image:
        context['profile_photo'] = request.user.funcionario.image.url
    return context


def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        obj.criado_em = obj.criado_em.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([getattr(obj, field) for field in field_names])
    return response


def export_xlsx(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{meta}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('meta')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(field_names)):
        ws.write(row_num, col_num, field_names[col_num], font_style)

    default_style = xlwt.XFStyle()
    rows = queryset.values_list()
    rows = [[x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, datetime) else x for x in row] for row in rows]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], default_style)

    wb.save(response)
    return response


def salva_criado_por(request, obj):
    if not obj.pk:
        obj.criado_por = request.user
    else:
        obj.atualizado_por = request.user
    obj.save()


def send_email_logs():
    logger.info('Email enviado com sucesso!')
    filename = 'logs.log'

    email_default = settings.DEFAULT_FROM_EMAIL

    with open(filename) as logfile:
        mail.EmailMessage(
            'Novo log gerado',
            'Mensagem de teste de envio de email do Django',
            email_default,
            [email_default],
            attachments=[(filename, logfile.read(), 'text/plain')]
        ).send()


def teste_logging():
    logger.warning("Resposta do teste de logging warning")
    # logger_django.info("INFO = Mostra os logs do django")
    # logger_django.warning("WARNING = Mostra os logs do django")