# agendamento/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_semana_range(agendamentos):
    """Retorna o range de datas da semana"""
    if agendamentos:
        datas_inicio = [ag.data_inicio for ag in agendamentos]
        datas_fim = [ag.data_fim for ag in agendamentos]
        todas_datas = datas_inicio + datas_fim
        return f"{min(todas_datas).strftime('%d/%m/%Y')} a {max(todas_datas).strftime('%d/%m/%Y')}"
    return ""

@register.filter
def get_ultimo_item(lista):
    """Retorna o último item de uma lista"""
    if lista:
        return lista[-1]
    return None