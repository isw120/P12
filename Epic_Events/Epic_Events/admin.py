from django.contrib import admin
from .models import User, Client, Contract, Event


class UserFields(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'role']


class ClientFields(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'is_confirmed_client']


class ContractFields(admin.ModelAdmin):
    list_display = ['client', 'name', 'description', 'amount', 'is_signed']


class EventFields(admin.ModelAdmin):
    list_display = ['client', 'name', 'description', 'guests_number', 'event_date', 'is_finished']


admin.site.register(User, UserFields)
admin.site.register(Client, ClientFields)
admin.site.register(Contract, ContractFields)
admin.site.register(Event, EventFields)
