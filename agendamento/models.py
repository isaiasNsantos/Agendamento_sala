from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Sala(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome da Sala')
    capacidade = models.PositiveIntegerField(verbose_name='Capacidade')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    ativa = models.BooleanField(default=True, verbose_name='Sala ativa')

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"{self.nome} (Capacidade: {self.capacidade})"

class Agendamento(models.Model):
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name='Sala')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')
    data_inicio = models.DateField(verbose_name='Data inicial do agendamento')
    data_fim = models.DateField(verbose_name='Data final do agendamento')
    hora_inicio = models.TimeField(verbose_name='Hora de início')
    hora_fim = models.TimeField(verbose_name='Hora de término')
    descricao = models.TextField(verbose_name='Descrição do agendamento')
    data_criacao = models.DateTimeField(default=timezone.now, verbose_name='Data de criação')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
        ordering = ['data_inicio', 'hora_inicio']

    def __str__(self):
        if self.data_inicio == self.data_fim:
            return f"{self.sala.nome} - {self.data_inicio} {self.hora_inicio}-{self.hora_fim} - {self.usuario.username}"
        else:
            return f"{self.sala.nome} - {self.data_inicio} a {self.data_fim} {self.hora_inicio}-{self.hora_fim} - {self.usuario.username}"