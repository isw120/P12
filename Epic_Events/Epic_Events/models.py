from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    roles = [('Gestion', 'Gestion'), ('Vente', 'Vente'), ('Support', 'Support')]

    role = models.CharField(choices=roles, max_length=255, default="Gestion")

    def save(self, *args, **kwargs):
        user = super(User, self)
        if len(user.password) != 88:
            user.set_password(user.password)
        super(User, self).save(*args, **kwargs)
        return user


class Client(models.Model):
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'}, blank=True,
                                   null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    is_confirmed_client = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.first_name


class Contract(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'}, blank=True,
                                   null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    is_signed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        try:
            self.client is not None
        except Client.DoesNotExist:
            raise ValidationError('A contract must have a client to be created')

        if self.client.is_confirmed_client:
            return True
        else:
            raise ValidationError('This client is not a confirmed client yet')


class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'},
                                   related_name="sales_user", blank=True, null=True)
    support_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Support'},
                                     related_name="support_user", blank=True, null=True)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    guests_number = models.IntegerField(validators=[MinValueValidator(1)])
    event_date = models.DateTimeField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):

        if self.contract.is_signed:
            return True
        else:
            raise ValidationError('The event cannot be created until it\'s contract is signed')
