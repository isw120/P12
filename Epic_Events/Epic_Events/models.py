from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    roles = [
        ('Gestion', 'Gestion'),
        ('Vente', 'Vente'),
        ('Support', 'Support'),
    ]

    role = models.CharField(choices=roles, max_length=255, default="Gestion")

    def save(self, *args, **kwargs):
        user = super(Users, self)
        if len(user.password) != 88:
            user.set_password(user.password)
        super(Users, self).save(*args, **kwargs)
        return user

