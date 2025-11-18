from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate, logout  # Adicione logout aqui
from django.db import models

class CustomUser(AbstractUser):
    matricula = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Matrícula'
    )
    departamento = models.CharField(
        max_length=100,
        verbose_name='Departamento'
    )

    def __str__(self):
        return f"{self.username} - {self.matricula}"

       
