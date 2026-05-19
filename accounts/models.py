import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        MICROEMPRESARIO = 'MICROEMPRESARIO', 'Microempresario'
        COMPRADOR = 'COMPRADOR', 'Comprador'
        ADMIN = 'ADMIN', 'Administrador'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.COMPRADOR)
    region = models.ForeignKey('products.Region', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email