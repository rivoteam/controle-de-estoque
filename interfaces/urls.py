from django.contrib import admin
from django.urls import path
from .views import homepage, appvendas

urlpatterns = [
    path('', homepage, name="homepage"),
    path('app-vendas', appvendas, name="appvendas"),
]
