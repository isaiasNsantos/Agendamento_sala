# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
#     path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
#     path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
#     path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
#     path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
#     path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
#     path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
# ]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
#     path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
#     path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
#     path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
    
#     # APIs para o calendário
#     path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
#     path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
#     path('meus-agendamentos/', views.meus_agendamentos, name='meus_agendamentos'),
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
#     path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
#     path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
    
#     # APIs para o calendário
#     path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
#     path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
    
#     # ATUALIZE ESTA LINHA ↓ (de meus-agendamentos para agendamentos)
#     path('agendamentos/', views.meus_agendamentos, name='lista_agendamentos'),
    
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
#     path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
#     path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
    
#     # APIs para o calendário
#     path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
#     path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
    
#     # Relatórios (NOVAS URLs)
#     path('relatorios/', views.relatorios_agendamentos, name='relatorios'),
#     path('relatorios/exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
#     path('relatorios/exportar-excel/', views.exportar_excel, name='exportar_excel'),
# ]

# agendamento/urls.py

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.pagina_inicial, name='pagina_inicial'),
#     path('salas/', views.lista_salas, name='lista_salas'),
#     path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
#     path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
#     path('agendamentos/', views.meus_agendamentos, name='lista_agendamentos'),
#     path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
#     path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
#     path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
#     path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
    
#     # APIs para o calendário
#     path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
#     path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
    
#     # Relatórios (NOVAS URLs)
#     path('relatorios/', views.relatorios_agendamentos, name='relatorios'),
#     path('relatorios/exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
#     path('relatorios/exportar-excel/', views.exportar_excel, name='exportar_excel'),
#     # urls.py
#     path('calendario/', views.calendario_agendamentos, name='calendario_agendamentos'),
# ]

# agendamento/urls.py - VERSÃO CORRIGIDA

from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('salas/', views.lista_salas, name='lista_salas'),
    path('novo-agendamento/', views.criar_agendamento, name='criar_agendamento'),
    path('novo-agendamento/<int:sala_id>/', views.criar_agendamento, name='criar_agendamento_sala'),
    path('agendamentos/', views.meus_agendamentos, name='lista_agendamentos'),
    path('editar-agendamento/<int:agendamento_id>/', views.editar_agendamento, name='editar_agendamento'),
    path('excluir-agendamento/<int:agendamento_id>/', views.excluir_agendamento, name='excluir_agendamento'),
    path('disponibilidade/', views.disponibilidade_salas, name='disponibilidade_salas'),
    path('disponibilidade/<str:data>/', views.disponibilidade_salas, name='disponibilidade_salas_data'),
    
    # APIs para o calendário
    path('api/dias-ocupados/<int:sala_id>/', views.api_dias_ocupados, name='api_dias_ocupados'),
    path('api/verificar-disponibilidade/<int:sala_id>/', views.api_verificar_disponibilidade, name='api_verificar_disponibilidade'),
    
    # Relatórios
    path('relatorios/', views.relatorios_agendamentos, name='relatorios'),
    path('relatorios/exportar-pdf/', views.exportar_pdf, name='exportar_pdf'),
    path('relatorios/exportar-excel/', views.exportar_excel, name='exportar_excel'),
    
    # NOVA URL DO CALENDÁRIO - CORRIGIDA
    path('calendario/', views.calendario_agendamentos, name='calendario_agendamentos'),
]