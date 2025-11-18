# agendamento/utils.py
from datetime import timedelta
from django.utils import timezone
from calendar import monthrange
from .models import Agendamento

def verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim, agendamento_id=None):
    """
    Verifica a disponibilidade de uma sala em um período específico
    Retorna uma lista de datas com conflitos
    """
    conflitos = []
    current_date = data_inicio
    
    while current_date <= data_fim:
        # Verificar se há agendamentos conflitantes nesta data
        agendamentos_conflitantes = Agendamento.objects.filter(
            sala=sala,
            data_inicio__lte=current_date,
            data_fim__gte=current_date
        ).exclude(pk=agendamento_id)
        
        for agendamento in agendamentos_conflitantes:
            if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
                conflitos.append({
                    'data': current_date,
                    'agendamento': agendamento
                })
                break
        
        current_date += timedelta(days=1)
    
    return conflitos

def obter_dias_ocupados(sala, mes, ano):
    """
    Retorna os dias do mês que estão ocupados para uma sala específica
    """
    _, ultimo_dia = monthrange(ano, mes)
    
    primeiro_dia_mes = timezone.datetime(ano, mes, 1).date()
    ultimo_dia_mes = timezone.datetime(ano, mes, ultimo_dia).date()
    
    # Buscar agendamentos que se sobrepõem com o mês
    agendamentos = Agendamento.objects.filter(
        sala=sala,
        data_inicio__lte=ultimo_dia_mes,
        data_fim__gte=primeiro_dia_mes
    )
    
    dias_ocupados = set()
    
    for agendamento in agendamentos:
        # Determinar os dias dentro do mês que estão ocupados
        inicio = max(agendamento.data_inicio, primeiro_dia_mes)
        fim = min(agendamento.data_fim, ultimo_dia_mes)
        
        current = inicio
        while current <= fim:
            dias_ocupados.add(current.day)
            current += timedelta(days=1)
    
    return list(dias_ocupados)