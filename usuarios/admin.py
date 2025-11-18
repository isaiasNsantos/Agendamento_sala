from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'matricula', 'departamento', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('matricula', 'departamento')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('matricula', 'departamento')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)