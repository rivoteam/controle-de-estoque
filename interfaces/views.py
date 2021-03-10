from django.shortcuts import render
from core.settings import STATIC_URL


def homepage(request):
    context = {
        'profile_photo': STATIC_URL + 'img/theme/avocado.png',
        'fullname': f'{request.user.first_name} {request.user.last_name}',
    }
    if request.user.first_name == "":
        context['fullname'] = request.user.username
    if request.user.funcionario.image:
        context['profile_photo'] = request.user.funcionario.image.url
    return render(request, 'homepage.html', context)
