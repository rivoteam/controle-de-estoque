from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Funcionario, CargoFuncionario


class ProfileInline(admin.StackedInline):
    model = Funcionario
    can_delete = False
    verbose_name_plural = 'Funcionarios'
    fk_name = 'funcionario'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)


@admin.register(CargoFuncionario)
class CargoFuncionarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created', 'updated']
    search_fields = ['name', 'slug']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
