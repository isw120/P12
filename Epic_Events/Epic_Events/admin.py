from django.contrib import admin
from .models import Users


class UsersFields(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'role']

admin.site.register(Users, UsersFields)

