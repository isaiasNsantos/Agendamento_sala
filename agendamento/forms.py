# from django import forms
# from .models import Agendamento, Sala
# from django.utils import timezone
# from django.core.exceptions import ValidationError
# from datetime import timedelta
# # views.py - Adicione estas importações no TOPO do arquivo
# from django.http import JsonResponse
# from datetime import datetime
# from .forms import verificar_disponibilidade_sala, obter_dias_ocupados  # IMPORTANTE: Adicione esta linha

# # ... resto do código existente ...

# @login_required
# def api_dias_ocupados(request, sala_id):
#     """
#     API que retorna os dias ocupados de uma sala para um mês específico
#     """
#     sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
#     mes = int(request.GET.get('mes', datetime.now().month))
#     ano = int(request.GET.get('ano', datetime.now().year))
    
#     dias_ocupados = obter_dias_ocupados(sala, mes, ano)
    
#     return JsonResponse({
#         'sala_id': sala_id,
#         'sala_nome': sala.nome,
#         'mes': mes,
#         'ano': ano,
#         'dias_ocupados': dias_ocupados,
#         'total_dias_ocupados': len(dias_ocupados)
#     })

# @login_required
# def api_verificar_disponibilidade(request, sala_id):
#     """
#     API para verificar disponibilidade em tempo real
#     """
#     sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
#     data_inicio = request.GET.get('data_inicio')
#     data_fim = request.GET.get('data_fim')
#     hora_inicio = request.GET.get('hora_inicio')
#     hora_fim = request.GET.get('hora_fim')
    
#     if not all([data_inicio, data_fim, hora_inicio, hora_fim]):
#         return JsonResponse({'error': 'Parâmetros incompletos'}, status=400)
    
#     try:
#         data_inicio = timezone.datetime.strptime(data_inicio, '%Y-%m-%d').date()
#         data_fim = timezone.datetime.strptime(data_fim, '%Y-%m-%d').date()
#         hora_inicio = timezone.datetime.strptime(hora_inicio, '%H:%M').time()
#         hora_fim = timezone.datetime.strptime(hora_fim, '%H:%M').time()
#     except ValueError:
#         return JsonResponse({'error': 'Formato de data/hora inválido'}, status=400)
    
#     conflitos = verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim)
    
#     return JsonResponse({
#         'disponivel': len(conflitos) == 0,
#         'total_conflitos': len(conflitos),
#         'conflitos': [
#             {
#                 'data': conflito['data'].strftime('%d/%m/%Y'),
#                 'responsavel': conflito['agendamento'].usuario.username,
#                 'horario': f"{conflito['agendamento'].hora_inicio.strftime('%H:%M')} - {conflito['agendamento'].hora_fim.strftime('%H:%M')}"
#             }
#             for conflito in conflitos
#         ]
#     })

# class AgendamentoForm(forms.ModelForm):
#     class Meta:
#         model = Agendamento
#         fields = ['sala', 'data_inicio', 'data_fim', 'hora_inicio', 'hora_fim', 'descricao']
#         widgets = {
#             'data_inicio': forms.DateInput(attrs={'type': 'date'}),
#             'data_fim': forms.DateInput(attrs={'type': 'date'}),
#             'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
#             'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
#             'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o propósito do agendamento'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['sala'].queryset = Sala.objects.filter(ativa=True)
        
#         hoje = timezone.now().date()
#         self.fields['data_inicio'].widget.attrs['min'] = hoje
#         self.fields['data_fim'].widget.attrs['min'] = hoje
#         self.fields['hora_inicio'].widget.attrs['min'] = '06:00'
#         self.fields['hora_fim'].widget.attrs['max'] = '22:00'

#     def clean_data_inicio(self):
#         data_inicio = self.cleaned_data.get('data_inicio')
#         if data_inicio and data_inicio < timezone.now().date():
#             raise ValidationError("❌ Não é possível agendar para datas passadas.")
#         return data_inicio

#     def clean_data_fim(self):
#         data_fim = self.cleaned_data.get('data_fim')
#         data_inicio = self.cleaned_data.get('data_inicio')
        
#         if data_inicio and data_fim and data_fim < data_inicio:
#             raise ValidationError("❌ A data final deve ser posterior ou igual à data inicial.")
#         return data_fim

#     def clean_hora_inicio(self):
#         hora_inicio = self.cleaned_data.get('hora_inicio')
#         if hora_inicio:
#             hora_minima = timezone.datetime.strptime('06:00', '%H:%M').time()
#             if hora_inicio < hora_minima:
#                 raise ValidationError("❌ O horário mínimo para agendamento é 06:00.")
#         return hora_inicio

#     def clean_hora_fim(self):
#         hora_fim = self.cleaned_data.get('hora_fim')
#         hora_inicio = self.cleaned_data.get('hora_inicio')
        
#         if hora_inicio and hora_fim:
#             if hora_fim <= hora_inicio:
#                 raise ValidationError("❌ A hora de término deve ser posterior à hora de início.")
            
#             # Calcular diferença em minutos
#             diferenca_minutos = (
#                 (hora_fim.hour * 60 + hora_fim.minute) - 
#                 (hora_inicio.hour * 60 + hora_inicio.minute)
#             )
            
#             if diferenca_minutos < 30:
#                 raise ValidationError("❌ O agendamento deve ter pelo menos 30 minutos de duração.")
        
#         return hora_fim

#     def clean(self):
#         cleaned_data = super().clean()
#         data_inicio = cleaned_data.get('data_inicio')
#         data_fim = cleaned_data.get('data_fim')
#         hora_inicio = cleaned_data.get('hora_inicio')
#         hora_fim = cleaned_data.get('hora_fim')
#         sala = cleaned_data.get('sala')

#         if all([data_inicio, data_fim, hora_inicio, hora_fim, sala]):
#             self.validar_conflitos_agendamento(sala, data_inicio, data_fim, hora_inicio, hora_fim)
#             self.validar_salas_especiais(sala, data_inicio, data_fim, hora_inicio, hora_fim)

#         return cleaned_data

#     def validar_conflitos_agendamento(self, sala, data_inicio, data_fim, hora_inicio, hora_fim):
#         """Valida conflitos de agendamento para a mesma sala"""
#         current_date = data_inicio
#         while current_date <= data_fim:
#             conflitos = Agendamento.objects.filter(
#                 sala=sala,
#                 data_inicio__lte=current_date,
#                 data_fim__gte=current_date
#             ).exclude(pk=self.instance.pk if self.instance else None)
            
#             for agendamento in conflitos:
#                 if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
#                     raise ValidationError(
#                         f"🚫 Conflito de horário! A sala {sala.nome} já está agendada para o dia {current_date.strftime('%d/%m/%Y')}.\n"
#                         f"📅 Período: {agendamento.data_inicio.strftime('%d/%m/%Y')} a {agendamento.data_fim.strftime('%d/%m/%Y')}\n"
#                         f"🕐 Horário: {agendamento.hora_inicio.strftime('%H:%M')} - {agendamento.hora_fim.strftime('%H:%M')}\n"
#                         f"👤 Responsável: {agendamento.usuario.username}"
#                     )
#             current_date += timedelta(days=1)

#     def validar_salas_especiais(self, sala, data_inicio, data_fim, hora_inicio, hora_fim):
#         """Valida regras específicas para salas especiais"""
#         nome_sala = sala.nome
        
#         if nome_sala == 'Minhoto_Sonho':
#             self.validar_sala_completa(data_inicio, data_fim, hora_inicio, hora_fim)
#         elif nome_sala in ['Minhoto', 'Sonho']:
#             self.validar_sala_individual(nome_sala, data_inicio, data_fim, hora_inicio, hora_fim)

#     def validar_sala_completa(self, data_inicio, data_fim, hora_inicio, hora_fim):
#         """Valida se pode agendar a sala completa (Minhoto_Sonho)"""
#         salas_individuais = ['Minhoto', 'Sonho']
#         current_date = data_inicio
        
#         while current_date <= data_fim:
#             conflitos = Agendamento.objects.filter(
#                 sala__nome__in=salas_individuais,
#                 data_inicio__lte=current_date,
#                 data_fim__gte=current_date
#             ).exclude(pk=self.instance.pk if self.instance else None)
            
#             for conflito in conflitos:
#                 if (hora_inicio < conflito.hora_fim and hora_fim > conflito.hora_inicio):
#                     raise ValidationError(
#                         f"🚫 Não é possível agendar a sala completa (Minhoto_Sonho)!\n\n"
#                         f"📋 A sala {conflito.sala.nome} já está agendada no dia {current_date.strftime('%d/%m/%Y')}:\n"
#                         f"   📅 Período: {conflito.data_inicio.strftime('%d/%m/%Y')} a {conflito.data_fim.strftime('%d/%m/%Y')}\n"
#                         f"   🕐 Horário: {conflito.hora_inicio.strftime('%H:%M')} - {conflito.hora_fim.strftime('%H:%M')}\n"
#                         f"   👤 Responsável: {conflito.usuario.username}\n\n"
#                         f"💡 Dica: A sala Minhoto_Sonho não pode ser agendada quando as salas individuais estão ocupadas."
#                     )
#             current_date += timedelta(days=1)

#     def validar_sala_individual(self, nome_sala, data_inicio, data_fim, hora_inicio, hora_fim):
#         """Valida se pode agendar sala individual (Minhoto ou Sonho)"""
#         current_date = data_inicio
        
#         while current_date <= data_fim:
#             conflitos = Agendamento.objects.filter(
#                 sala__nome='Minhoto_Sonho',
#                 data_inicio__lte=current_date,
#                 data_fim__gte=current_date
#             ).exclude(pk=self.instance.pk if self.instance else None)
            
#             for conflito in conflitos:
#                 if (hora_inicio < conflito.hora_fim and hora_fim > conflito.hora_inicio):
#                     raise ValidationError(
#                         f"🚫 Não é possível agendar a sala {nome_sala}!\n\n"
#                         f"📋 A sala completa (Minhoto_Sonho) já está agendada no dia {current_date.strftime('%d/%m/%Y')}:\n"
#                         f"   📅 Período: {conflito.data_inicio.strftime('%d/%m/%Y')} a {conflito.data_fim.strftime('%d/%m/%Y')}\n"
#                         f"   🕐 Horário: {conflito.hora_inicio.strftime('%H:%M')} - {conflito.hora_fim.strftime('%H:%M')}\n"
#                         f"   👤 Responsável: {conflito.usuario.username}\n\n"
#                         f"💡 Dica: As salas individuais não podem ser agendadas quando a sala completa está reservada."
#                     )
#             current_date += timedelta(days=1)

# # Adicionar estas funções ao forms.py (após a classe AgendamentoForm)

# def verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim, agendamento_id=None):
#     """
#     Verifica a disponibilidade de uma sala em um período específico
#     Retorna uma lista de datas com conflitos
#     """
#     conflitos = []
#     current_date = data_inicio
    
#     while current_date <= data_fim:
#         # Verificar se há agendamentos conflitantes nesta data
#         agendamentos_conflitantes = Agendamento.objects.filter(
#             sala=sala,
#             data_inicio__lte=current_date,
#             data_fim__gte=current_date
#         ).exclude(pk=agendamento_id)
        
#         for agendamento in agendamentos_conflitantes:
#             if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
#                 conflitos.append({
#                     'data': current_date,
#                     'agendamento': agendamento
#                 })
#                 break  # Só precisa de um conflito por data
        
#         current_date += timedelta(days=1)
    
#     return conflitos

# def obter_dias_ocupados(sala, mes, ano):
#     """
#     Retorna os dias do mês que estão ocupados para uma sala específica
#     """
#     from calendar import monthrange
#     _, ultimo_dia = monthrange(ano, mes)
    
#     primeiro_dia_mes = timezone.datetime(ano, mes, 1).date()
#     ultimo_dia_mes = timezone.datetime(ano, mes, ultimo_dia).date()
    
#     # Buscar agendamentos que se sobrepõem com o mês
#     agendamentos = Agendamento.objects.filter(
#         sala=sala,
#         data_inicio__lte=ultimo_dia_mes,
#         data_fim__gte=primeiro_dia_mes
#     )
    
#     dias_ocupados = set()
    
#     for agendamento in agendamentos:
#         # Determinar os dias dentro do mês que estão ocupados
#         inicio = max(agendamento.data_inicio, primeiro_dia_mes)
#         fim = min(agendamento.data_fim, ultimo_dia_mes)
        
#         current = inicio
#         while current <= fim:
#             dias_ocupados.add(current.day)
#             current += timedelta(days=1)
    
#     return list(dias_ocupados)

from django import forms
from .models import Agendamento, Sala
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['sala', 'data_inicio', 'data_fim', 'hora_inicio', 'hora_fim', 'descricao']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'descricao': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Descreva o propósito do agendamento'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sala'].queryset = Sala.objects.filter(ativa=True)
        
        hoje = timezone.now().date()
        self.fields['data_inicio'].widget.attrs['min'] = hoje
        self.fields['data_fim'].widget.attrs['min'] = hoje
        self.fields['hora_inicio'].widget.attrs['min'] = '06:00'
        self.fields['hora_fim'].widget.attrs['max'] = '22:00'

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        if data_inicio and data_inicio < timezone.now().date():
            raise ValidationError("❌ Não é possível agendar para datas passadas.")
        return data_inicio

    def clean_data_fim(self):
        data_fim = self.cleaned_data.get('data_fim')
        data_inicio = self.cleaned_data.get('data_inicio')
        
        if data_inicio and data_fim and data_fim < data_inicio:
            raise ValidationError("❌ A data final deve ser posterior ou igual à data inicial.")
        return data_fim

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio:
            hora_minima = timezone.datetime.strptime('06:00', '%H:%M').time()
            if hora_inicio < hora_minima:
                raise ValidationError("❌ O horário mínimo para agendamento é 06:00.")
        return hora_inicio

    def clean_hora_fim(self):
        hora_fim = self.cleaned_data.get('hora_fim')
        hora_inicio = self.cleaned_data.get('hora_inicio')
        
        if hora_inicio and hora_fim:
            if hora_fim <= hora_inicio:
                raise ValidationError("❌ A hora de término deve ser posterior à hora de início.")
            
            # Calcular diferença em minutos
            diferenca_minutos = (
                (hora_fim.hour * 60 + hora_fim.minute) - 
                (hora_inicio.hour * 60 + hora_inicio.minute)
            )
            
            if diferenca_minutos < 30:
                raise ValidationError("❌ O agendamento deve ter pelo menos 30 minutos de duração.")
        
        return hora_fim

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')
        sala = cleaned_data.get('sala')

        if all([data_inicio, data_fim, hora_inicio, hora_fim, sala]):
            self.validar_conflitos_agendamento(sala, data_inicio, data_fim, hora_inicio, hora_fim)
            self.validar_salas_especiais(sala, data_inicio, data_fim, hora_inicio, hora_fim)

        return cleaned_data

    def validar_conflitos_agendamento(self, sala, data_inicio, data_fim, hora_inicio, hora_fim):
        """Valida conflitos de agendamento para a mesma sala"""
        current_date = data_inicio
        while current_date <= data_fim:
            conflitos = Agendamento.objects.filter(
                sala=sala,
                data_inicio__lte=current_date,
                data_fim__gte=current_date
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            for agendamento in conflitos:
                if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
                    raise ValidationError(
                        f"🚫 Conflito de horário! A sala {sala.nome} já está agendada para o dia {current_date.strftime('%d/%m/%Y')}.\n"
                        f"📅 Período: {agendamento.data_inicio.strftime('%d/%m/%Y')} a {agendamento.data_fim.strftime('%d/%m/%Y')}\n"
                        f"🕐 Horário: {agendamento.hora_inicio.strftime('%H:%M')} - {agendamento.hora_fim.strftime('%H:%M')}\n"
                        f"👤 Responsável: {agendamento.usuario.username}"
                    )
            current_date += timedelta(days=1)

    def validar_salas_especiais(self, sala, data_inicio, data_fim, hora_inicio, hora_fim):
        """Valida regras específicas para salas especiais"""
        nome_sala = sala.nome
        
        if nome_sala == 'Minhoto_Sonho':
            self.validar_sala_completa(data_inicio, data_fim, hora_inicio, hora_fim)
        elif nome_sala in ['Minhoto', 'Sonho']:
            self.validar_sala_individual(nome_sala, data_inicio, data_fim, hora_inicio, hora_fim)

    def validar_sala_completa(self, data_inicio, data_fim, hora_inicio, hora_fim):
        """Valida se pode agendar a sala completa (Minhoto_Sonho)"""
        salas_individuais = ['Minhoto', 'Sonho']
        current_date = data_inicio
        
        while current_date <= data_fim:
            conflitos = Agendamento.objects.filter(
                sala__nome__in=salas_individuais,
                data_inicio__lte=current_date,
                data_fim__gte=current_date
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            for conflito in conflitos:
                if (hora_inicio < conflito.hora_fim and hora_fim > conflito.hora_inicio):
                    raise ValidationError(
                        f"🚫 Não é possível agendar a sala completa (Minhoto_Sonho)!\n\n"
                        f"📋 A sala {conflito.sala.nome} já está agendada no dia {current_date.strftime('%d/%m/%Y')}:\n"
                        f"   📅 Período: {conflito.data_inicio.strftime('%d/%m/%Y')} a {conflito.data_fim.strftime('%d/%m/%Y')}\n"
                        f"   🕐 Horário: {conflito.hora_inicio.strftime('%H:%M')} - {conflito.hora_fim.strftime('%H:%M')}\n"
                        f"   👤 Responsável: {conflito.usuario.username}\n\n"
                        f"💡 Dica: A sala Minhoto_Sonho não pode ser agendada quando as salas individuais estão ocupadas."
                    )
            current_date += timedelta(days=1)

    def validar_sala_individual(self, nome_sala, data_inicio, data_fim, hora_inicio, hora_fim):
        """Valida se pode agendar sala individual (Minhoto ou Sonho)"""
        current_date = data_inicio
        
        while current_date <= data_fim:
            conflitos = Agendamento.objects.filter(
                sala__nome='Minhoto_Sonho',
                data_inicio__lte=current_date,
                data_fim__gte=current_date
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            for conflito in conflitos:
                if (hora_inicio < conflito.hora_fim and hora_fim > conflito.hora_inicio):
                    raise ValidationError(
                        f"🚫 Não é possível agendar a sala {nome_sala}!\n\n"
                        f"📋 A sala completa (Minhoto_Sonho) já está agendada no dia {current_date.strftime('%d/%m/%Y')}:\n"
                        f"   📅 Período: {conflito.data_inicio.strftime('%d/%m/%Y')} a {conflito.data_fim.strftime('%d/%m/%Y')}\n"
                        f"   🕐 Horário: {conflito.hora_inicio.strftime('%H:%M')} - {conflito.hora_fim.strftime('%H:%M')}\n"
                        f"   👤 Responsável: {conflito.usuario.username}\n\n"
                        f"💡 Dica: As salas individuais não podem ser agendadas quando a sala completa está reservada."
                    )
            current_date += timedelta(days=1)