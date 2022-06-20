from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    roles = [
        ('Gestion', 'Gestion'),
        ('Vente', 'Vente'),
        ('Support', 'Support'),
    ]

    role = models.CharField(choices=roles, max_length=255, default="Gestion")

    def save(self, *args, **kwargs):
        user = super(User, self)
        if len(user.password) != 88:
            user.set_password(user.password)
        super(User, self).save(*args, **kwargs)
        return user

class Client(models.Model):
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'})
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    compagny_name = models.CharField(max_length=255)
    is_confirmed_client = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class Contract(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'})
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_signed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    sales_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Vente'}, related_name="sales_user")
    support_user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, limit_choices_to={'role': 'Support'}, related_name="support_user")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    is_finished = models.BooleanField(default=False)
    event_date = models.DateTimeField()
    guests = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name