from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Funcionario


class ProfileInline(admin.StackedInline):
    model = Funcionario
    can_delete = False
    verbose_name_plural = 'Funcionarios'
    fk_name = 'funcionario'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
