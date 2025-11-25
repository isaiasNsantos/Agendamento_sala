# agendamento/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Sala, Agendamento
from django.utils import timezone

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'capacidade', 'ativa', 'colored_status', 'tipo_sala']
    list_filter = ['ativa', 'nome']
    search_fields = ['nome']
    list_editable = ['ativa']
    
    def colored_status(self, obj):
        if obj.ativa:
            return format_html(
                '<span style="color: green; font-weight: bold;">● ATIVA</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">● INATIVA</span>'
            )
    colored_status.short_description = 'Status'
    
    def tipo_sala(self, obj):
        if obj.nome in ['Minhoto', 'Sonho', 'Minhoto_Sonho']:
            return format_html(
                '<span style="background: #f39c12; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">⭐ ESPECIAL</span>'
            )
        else:
            return format_html(
                '<span style="background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">🏢 COMUM</span>'
            )
    tipo_sala.short_description = 'Tipo'

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ['sala', 'usuario', 'data_inicio', 'data_fim', 'hora_inicio', 'hora_fim', 'status_agendamento']
    list_filter = ['data_inicio', 'sala', 'usuario']
    date_hierarchy = 'data_inicio'
    search_fields = ['sala__nome', 'usuario__username', 'descricao']
    readonly_fields = ['data_criacao']
    
    fieldsets = (
        ('Informações da Sala', {
            'fields': ('sala', 'usuario')
        }),
        ('Período do Agendamento', {
            'fields': ('data_inicio', 'data_fim', 'hora_inicio', 'hora_fim')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'data_criacao')
        }),
    )
    
    def status_agendamento(self, obj):
        hoje = timezone.now().date()
        
        if obj.data_fim < hoje:
            return format_html(
                '<span style="background: #95a5a6; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">⏹️ CONCLUÍDO</span>'
            )
        elif obj.data_inicio > hoje:
            return format_html(
                '<span style="background: #3498db; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">⏳ FUTURO</span>'
            )
        else:
            return format_html(
                '<span style="background: #2ecc71; color: white; padding: 4px 8px; border-radius: 12px; font-weight: bold;">▶️ ATIVO</span>'
            )
    status_agendamento.short_description = 'Status'