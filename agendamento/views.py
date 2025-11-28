# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Sala, Agendamento
# from .forms import AgendamentoForm
# from django.utils import timezone
# from datetime import timedelta
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse
# from datetime import datetime
# from calendar import monthrange
# # Adicionar ao views.py (após as views existentes)

# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import pandas as pd
# from datetime import datetime
# import tempfile
# from django.db.models import Q

# # views.py - SUBSTITUA as importações do weasyprint

# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Sala, Agendamento
# from .forms import AgendamentoForm
# from django.utils import timezone
# from datetime import timedelta
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import JsonResponse, HttpResponse
# from datetime import datetime
# from calendar import monthrange

# # NOVAS IMPORTACIONES PARA RELATÓRIOS - SUBSTITUINDO WEASYPRINT
# from io import BytesIO
# from django.template.loader import render_to_string
# from xhtml2pdf import pisa
# import pandas as pd
# import tempfile
# from django.contrib.auth import get_user_model

# User = get_user_model()


# @login_required
# def calendario_agendamentos(request):
#     """
#     View para exibir agendamentos em formato de calendário estilo Google Calendar
#     """
#     from calendar import monthrange
    
#     # Obter parâmetros de mês/ano da URL
#     ano = int(request.GET.get('ano', timezone.now().year))
#     mes = int(request.GET.get('mes', timezone.now().month))
    
#     # Calcular primeiro e último dia do mês
#     _, ultimo_dia_mes = monthrange(ano, mes)
#     data_inicio_mes = timezone.datetime(ano, mes, 1).date()
#     data_fim_mes = timezone.datetime(ano, mes, ultimo_dia_mes).date()
    
#     # Buscar agendamentos do mês
#     agendamentos = Agendamento.objects.filter(
#         data_inicio__lte=data_fim_mes,
#         data_fim__gte=data_inicio_mes
#     ).order_by('data_inicio', 'hora_inicio')
    
#     # Preparar dados do calendário
#     primeiro_dia_semana = data_inicio_mes.weekday()  # 0=segunda, 6=domingo
#     dias_mes_anterior = primeiro_dia_semana
#     total_celulas = 42  # 6 semanas
    
#     # Calcular mês anterior e próximo
#     if mes == 1:
#         mes_anterior = 12
#         ano_anterior = ano - 1
#     else:
#         mes_anterior = mes - 1
#         ano_anterior = ano
        
#     if mes == 12:
#         mes_proximo = 1
#         ano_proximo = ano + 1
#     else:
#         mes_proximo = mes + 1
#         ano_proximo = ano
    
#     # Obter último dia do mês anterior
#     _, ultimo_dia_anterior = monthrange(ano_anterior, mes_anterior)
    
#     # Construir grid do calendário
#     dias_calendario = []
    
#     # Dias do mês anterior
#     for i in range(dias_mes_anterior):
#         dia = ultimo_dia_anterior - dias_mes_anterior + i + 1
#         dias_calendario.append({
#             'dia': dia,
#             'mes': mes_anterior,
#             'ano': ano_anterior,
#             'eh_mes_atual': False,
#             'agendamentos': []
#         })
    
#     # Dias do mês atual
#     for dia in range(1, ultimo_dia_mes + 1):
#         data_dia = timezone.datetime(ano, mes, dia).date()
#         agendamentos_dia = [
#             ag for ag in agendamentos 
#             if ag.data_inicio <= data_dia <= ag.data_fim
#         ]
        
#         dias_calendario.append({
#             'dia': dia,
#             'mes': mes,
#             'ano': ano,
#             'eh_mes_atual': True,
#             'data': data_dia,
#             'agendamentos': agendamentos_dia,
#             'eh_hoje': data_dia == timezone.now().date()
#         })
    
#     # Dias do próximo mês
#     dias_restantes = total_celulas - len(dias_calendario)
#     for dia in range(1, dias_restantes + 1):
#         dias_calendario.append({
#             'dia': dia,
#             'mes': mes_proximo,
#             'ano': ano_proximo,
#             'eh_mes_atual': False,
#             'agendamentos': []
#         })
    
#     context = {
#         'ano': ano,
#         'mes': mes,
#         'mes_nome': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
#                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][mes-1],
#         'dias_calendario': dias_calendario,
#         'mes_anterior': mes_anterior,
#         'ano_anterior': ano_anterior,
#         'mes_proximo': mes_proximo,
#         'ano_proximo': ano_proximo,
#         'hoje': timezone.now().date(),
#         'salas': Sala.objects.filter(ativa=True),
#     }
    
#     return render(request, 'agendamento/calendario.html', context)

# @login_required
# def relatorios_agendamentos(request):
#     """
#     View principal de relatórios com filtros
#     """
#     # Filtros iniciais
#     data_inicio = request.GET.get('data_inicio')
#     data_fim = request.GET.get('data_fim')
#     sala_id = request.GET.get('sala')
#     usuario_id = request.GET.get('usuario')
    
#     # Query base
#     agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
#     # Aplicar filtros
#     if data_inicio:
#         agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
#     if data_fim:
#         agendamentos = agendamentos.filter(data_fim__lte=data_fim)
#     if sala_id:
#         agendamentos = agendamentos.filter(sala_id=sala_id)
#     if usuario_id:
#         agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
#     # Estatísticas para o relatório
#     total_agendamentos = agendamentos.count()
#     salas_utilizadas = agendamentos.values('sala__nome').distinct().count()
#     usuarios_ativos = agendamentos.values('usuario__username').distinct().count()
    
#     # Calcular duração para cada agendamento
#     for agendamento in agendamentos:
#         diff = agendamento.data_fim - agendamento.data_inicio
#         agendamento.duracao_dias = diff.days + 1
    
#     context = {
#         'agendamentos': agendamentos,
#         'salas': Sala.objects.filter(ativa=True),
#         'usuarios': User.objects.all(),
#         'total_agendamentos': total_agendamentos,
#         'salas_utilizadas': salas_utilizadas,
#         'usuarios_ativos': usuarios_ativos,
#         'filtros_aplicados': {
#             'data_inicio': data_inicio,
#             'data_fim': data_fim,
#             'sala_id': sala_id,
#             'usuario_id': usuario_id,
#         }
#     }
    
#     return render(request, 'agendamento/relatorios.html', context)

# @login_required
# def exportar_pdf(request):
#     """
#     Exportar relatório para PDF usando xhtml2pdf
#     """
#     # Reutilizar a mesma lógica de filtros da view principal
#     data_inicio = request.GET.get('data_inicio')
#     data_fim = request.GET.get('data_fim')
#     sala_id = request.GET.get('sala')
#     usuario_id = request.GET.get('usuario')
    
#     agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
#     if data_inicio:
#         agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
#     if data_fim:
#         agendamentos = agendamentos.filter(data_fim__lte=data_fim)
#     if sala_id:
#         agendamentos = agendamentos.filter(sala_id=sala_id)
#     if usuario_id:
#         agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
#     # Calcular estatísticas
#     total_agendamentos = agendamentos.count()
#     salas_utilizadas = agendamentos.values('sala__nome').distinct().count()
    
#     for agendamento in agendamentos:
#         diff = agendamento.data_fim - agendamento.data_inicio
#         agendamento.duracao_dias = diff.days + 1
    
#     context = {
#         'agendamentos': agendamentos,
#         'total_agendamentos': total_agendamentos,
#         'salas_utilizadas': salas_utilizadas,
#         'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M'),
#         'filtros_aplicados': {
#             'data_inicio': data_inicio,
#             'data_fim': data_fim,
#             'sala_id': sala_id,
#             'usuario_id': usuario_id,
#         }
#     }
    
#     # Renderizar HTML para PDF
#     html_string = render_to_string('agendamento/relatorio_pdf.html', context)
    
#     # Gerar PDF com xhtml2pdf
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.pdf"'
    
#     # Criar PDF
#     pisa_status = pisa.CreatePDF(
#         html_string,
#         dest=response,
#         encoding='UTF-8'
#     )
    
#     if pisa_status.err:
#         return HttpResponse('Erro ao gerar PDF: {}'.format(pisa_status.err))
    
#     return response

# @login_required
# def exportar_excel(request):
#     """
#     Exportar relatório para Excel
#     """
#     # Reutilizar a mesma lógica de filtros
#     data_inicio = request.GET.get('data_inicio')
#     data_fim = request.GET.get('data_fim')
#     sala_id = request.GET.get('sala')
#     usuario_id = request.GET.get('usuario')
    
#     agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
#     if data_inicio:
#         agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
#     if data_fim:
#         agendamentos = agendamentos.filter(data_fim__lte=data_fim)
#     if sala_id:
#         agendamentos = agendamentos.filter(sala_id=sala_id)
#     if usuario_id:
#         agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
#     # Preparar dados para Excel
#     dados = []
#     for agendamento in agendamentos:
#         diff = agendamento.data_fim - agendamento.data_inicio
#         duracao_dias = diff.days + 1
        
#         dados.append({
#             'Sala': agendamento.sala.nome,
#             'Usuário': agendamento.usuario.username,
#             'Data Início': agendamento.data_inicio.strftime('%d/%m/%Y'),
#             'Data Fim': agendamento.data_fim.strftime('%d/%m/%Y'),
#             'Horário Início': agendamento.hora_inicio.strftime('%H:%M'),
#             'Horário Fim': agendamento.hora_fim.strftime('%H:%M'),
#             'Duração (dias)': duracao_dias,
#             'Descrição': agendamento.descricao,
#             'Data Criação': agendamento.data_criacao.strftime('%d/%m/%Y %H:%M'),
#         })
    
#     # Criar DataFrame e Excel
#     df = pd.DataFrame(dados)
    
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
#             with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
#                 df.to_excel(writer, sheet_name='Agendamentos', index=False)
                
#                 # Formatar a planilha
#                 worksheet = writer.sheets['Agendamentos']
#                 for column in worksheet.columns:
#                     max_length = 0
#                     column_letter = column[0].column_letter
#                     for cell in column:
#                         try:
#                             if len(str(cell.value)) > max_length:
#                                 max_length = len(str(cell.value))
#                         except:
#                             pass
#                     adjusted_width = min(max_length + 2, 50)
#                     worksheet.column_dimensions[column_letter].width = adjusted_width
            
#             # Ler o arquivo temporário
#             with open(tmp.name, 'rb') as f:
#                 excel_data = f.read()
#     except Exception as e:
#         return HttpResponse(f'Erro ao gerar Excel: {str(e)}')
    
#     response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.xlsx"'
    
#     return response

# # Mantenha suas APIs existentes (api_dias_ocupados, api_verificar_disponibilidade)
# # ... [suas APIs existentes] ...


# def verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim, agendamento_id=None):
#     """
#     Verifica a disponibilidade de uma sala em um período específico
#     Considera as regras especiais para Minhoto_Sonho, Minhoto e Sonho
#     Retorna uma lista de datas com conflitos
#     """
#     conflitos = []
#     current_date = data_inicio
    
#     while current_date <= data_fim:
#         # Determinar quais salas verificar baseado nas regras especiais
#         if sala.nome == 'Minhoto_Sonho':
#             # Para Minhoto_Sonho: verificar também Minhoto e Sonho
#             salas_para_verificar = ['Minhoto_Sonho', 'Minhoto', 'Sonho']
#         elif sala.nome in ['Minhoto', 'Sonho']:
#             # Para salas individuais: verificar também Minhoto_Sonho
#             salas_para_verificar = ['Minhoto_Sonho', sala.nome]
#         else:
#             # Para outras salas: apenas a própria sala
#             salas_para_verificar = [sala.nome]
        
#         # Verificar se há agendamentos conflitantes nesta data
#         agendamentos_conflitantes = Agendamento.objects.filter(
#             sala__nome__in=salas_para_verificar,
#             data_inicio__lte=current_date,
#             data_fim__gte=current_date
#         ).exclude(pk=agendamento_id)
        
#         for agendamento in agendamentos_conflitantes:
#             if (hora_inicio < agendamento.hora_fim and hora_fim > agendamento.hora_inicio):
#                 conflitos.append({
#                     'data': current_date,
#                     'agendamento': agendamento
#                 })
#                 break
        
#         current_date += timedelta(days=1)
    
#     return conflitos


# def obter_dias_ocupados(sala, mes, ano):
#     """
#     Retorna os dias do mês que estão ocupados para uma sala específica
#     Considera as regras especiais para Minhoto_Sonho, Minhoto e Sonho
#     """
#     _, ultimo_dia = monthrange(ano, mes)
    
#     primeiro_dia_mes = timezone.datetime(ano, mes, 1).date()
#     ultimo_dia_mes = timezone.datetime(ano, mes, ultimo_dia).date()
    
#     # Buscar agendamentos que se sobrepõem com o mês
#     if sala.nome == 'Minhoto_Sonho':
#         # Para Minhoto_Sonho: também considerar ocupado quando Minhoto OU Sonho estiverem ocupadas
#         agendamentos = Agendamento.objects.filter(
#             data_inicio__lte=ultimo_dia_mes,
#             data_fim__gte=primeiro_dia_mes
#         ).filter(
#             sala__nome__in=['Minhoto_Sonho', 'Minhoto', 'Sonho']
#         )
#     elif sala.nome in ['Minhoto', 'Sonho']:
#         # Para salas individuais: também considerar ocupado quando Minhoto_Sonho estiver ocupada
#         agendamentos = Agendamento.objects.filter(
#             data_inicio__lte=ultimo_dia_mes,
#             data_fim__gte=primeiro_dia_mes
#         ).filter(
#             sala__nome__in=['Minhoto_Sonho', sala.nome]
#         )
#     else:
#         # Para outras salas: apenas agendamentos da própria sala
#         agendamentos = Agendamento.objects.filter(
#             sala=sala,
#             data_inicio__lte=ultimo_dia_mes,
#             data_fim__gte=primeiro_dia_mes
#         )
    
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

# # Views principais
# @login_required
# def pagina_inicial(request):
#     salas = Sala.objects.filter(ativa=True)
#     meus_agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data_inicio', '-hora_inicio')[:5]
    
#     return render(request, 'agendamento/inicio.html', {
#         'salas': salas,
#         'meus_agendamentos': meus_agendamentos
#     })

# @login_required
# def lista_salas(request):
#     salas = Sala.objects.filter(ativa=True)
    
#     # Paginação para salas
#     page = request.GET.get('page', 1)
#     paginator = Paginator(salas, 12)  # 12 salas por página
    
#     try:
#         salas_paginadas = paginator.page(page)
#     except PageNotAnInteger:
#         salas_paginadas = paginator.page(1)
#     except EmptyPage:
#         salas_paginadas = paginator.page(paginator.num_pages)
    
#     # Estatísticas
#     salas_ativas = salas.filter(ativa=True)
#     salas_especiais = salas.filter(nome__in=['Minhoto', 'Sonho', 'Minhoto_Sonho'])
    
#     return render(request, 'agendamento/lista_salas.html', {
#         'salas': salas_paginadas,
#         'salas_ativas': salas_ativas,
#         'salas_especiais': salas_especiais,
#     })

# @login_required
# def criar_agendamento(request, sala_id=None):
#     sala = None
#     if sala_id:
#         sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
#     if request.method == 'POST':
#         form = AgendamentoForm(request.POST)
#         if form.is_valid():
#             agendamento = form.save(commit=False)
#             agendamento.usuario = request.user
#             agendamento.save()
#             messages.success(request, 'Agendamento criado com sucesso!')
#             return redirect('pagina_inicial')
#         else:
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#     else:
#         initial = {'sala': sala} if sala else {}
#         form = AgendamentoForm(initial=initial)
    
#     salas = Sala.objects.filter(ativa=True)
#     return render(request, 'agendamento/criar_agendamento.html', {
#         'form': form,
#         'sala': sala,
#         'salas': salas
#     })

# @login_required
# def meus_agendamentos(request):
#     hoje = timezone.now().date()
    
#     # AGORA MOSTRA TODOS OS AGENDAMENTOS, NÃO APENAS DO USUÁRIO LOGADO
#     agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
#     # Paginação
#     page = request.GET.get('page', 1)
#     paginator = Paginator(agendamentos, 10)  # 10 agendamentos por página
    
#     try:
#         agendamentos_paginados = paginator.page(page)
#     except PageNotAnInteger:
#         agendamentos_paginados = paginator.page(1)
#     except EmptyPage:
#         agendamentos_paginados = paginator.page(paginator.num_pages)
    
#     # Calcular estatísticas (usando queryset original)
#     agendamentos_ativos = agendamentos.filter(data_fim__gte=hoje)
#     agendamentos_futuros = agendamentos.filter(data_inicio__gt=hoje)
#     agendamentos_passados = agendamentos.filter(data_fim__lt=hoje)
    
#     # Obter lista de salas únicas que têm agendamentos
#     salas_com_agendamentos = Sala.objects.filter(
#         id__in=agendamentos.values_list('sala', flat=True).distinct()
#     )
    
#     # Calcular duração em dias para cada agendamento na página atual
#     for agendamento in agendamentos_paginados:
#         diff = agendamento.data_fim - agendamento.data_inicio
#         agendamento.duracao_dias = diff.days + 1  # +1 para incluir o dia inicial
    
#     return render(request, 'agendamento/meus_agendamentos.html', {
#         'agendamentos': agendamentos_paginados,
#         'agendamentos_ativos': agendamentos_ativos,
#         'agendamentos_futuros': agendamentos_futuros,
#         'agendamentos_passados': agendamentos_passados,
#         'salas_com_agendamentos': salas_com_agendamentos,
#         'hoje': hoje
#     })


# @login_required
# def editar_agendamento(request, agendamento_id):
#     agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
#     if request.method == 'POST':
#         form = AgendamentoForm(request.POST, instance=agendamento)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Agendamento atualizado com sucesso!')
#             return redirect('meus_agendamentos')
#         else:
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#     else:
#         form = AgendamentoForm(instance=agendamento)
    
#     return render(request, 'agendamento/editar_agendamento.html', {
#         'form': form,
#         'agendamento': agendamento
#     })

# @login_required
# def excluir_agendamento(request, agendamento_id):
#     agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
#     if request.method == 'POST':
#         agendamento.delete()
#         messages.success(request, 'Agendamento excluído com sucesso!')
#         return redirect('meus_agendamentos')
    
#     return render(request, 'agendamento/excluir_agendamento.html', {
#         'agendamento': agendamento
#     })

# @login_required
# def disponibilidade_salas(request, data=None):
#     """
#     View para mostrar a disponibilidade de todas as salas em uma data específica
#     """
#     if not data:
#         data = timezone.now().date()
#     else:
#         try:
#             data = timezone.datetime.strptime(data, '%Y-%m-%d').date()
#         except ValueError:
#             data = timezone.now().date()
    
#     # Buscar todos os agendamentos que cobrem a data especificada
#     agendamentos = Agendamento.objects.filter(
#         data_inicio__lte=data,
#         data_fim__gte=data
#     ).order_by('sala__nome', 'hora_inicio')
    
#     # Organizar agendamentos por sala
#     agendamentos_por_sala = {}
#     for agendamento in agendamentos:
#         if agendamento.sala.nome not in agendamentos_por_sala:
#             agendamentos_por_sala[agendamento.sala.nome] = []
#         agendamentos_por_sala[agendamento.sala.nome].append(agendamento)
    
#     # Gerar horários do dia (das 06:00 às 22:00)
#     horarios = []
#     for hora in range(6, 22):
#         for minuto in [0, 30]:
#             horarios.append(f"{hora:02d}:{minuto:02d}")
    
#     # Calcular disponibilidade
#     salas = Sala.objects.filter(ativa=True)
    
#     # Criar uma estrutura de dados mais simples para o template
#     disponibilidade_simples = []
    
#     for horario in horarios:
#         hora_atual = timezone.datetime.strptime(horario, '%H:%M').time()
#         linha = {'horario': horario, 'salas': []}
        
#         for sala in salas:
#             # Verificar se há conflito neste horário
#             conflito = Agendamento.objects.filter(
#                 sala=sala,
#                 data_inicio__lte=data,
#                 data_fim__gte=data,
#                 hora_inicio__lte=hora_atual,
#                 hora_fim__gt=hora_atual
#             ).first()
            
#             if conflito:
#                 linha['salas'].append({
#                     'nome': sala.nome,
#                     'status': 'ocupado',
#                     'agendamento': conflito
#                 })
#             else:
#                 linha['salas'].append({
#                     'nome': sala.nome,
#                     'status': 'livre'
#                 })
        
#         disponibilidade_simples.append(linha)
    
#     return render(request, 'agendamento/disponibilidade.html', {
#         'data': data,
#         'agendamentos_por_sala': agendamentos_por_sala,
#         'disponibilidade_simples': disponibilidade_simples,
#         'horarios': horarios,
#         'salas': salas
#     })

# # APIs para o calendário
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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sala, Agendamento
from .forms import AgendamentoForm
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from datetime import datetime
from calendar import monthrange
# Adicionar ao views.py (após as views existentes)

from django.http import HttpResponse
from django.template.loader import render_to_string
import pandas as pd
from datetime import datetime
import tempfile
from django.db.models import Q

# views.py - SUBSTITUA as importações do weasyprint

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sala, Agendamento
from .forms import AgendamentoForm
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from calendar import monthrange

# NOVAS IMPORTACIONES PARA RELATÓRIOS - SUBSTITUINDO WEASYPRINT
from io import BytesIO
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import pandas as pd
import tempfile
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def calendario_agendamentos(request):
    """
    View para exibir agendamentos em formato de calendário estilo Google Calendar
    """
    from calendar import monthrange
    
    # Obter parâmetros de mês/ano da URL
    ano = int(request.GET.get('ano', timezone.now().year))
    mes = int(request.GET.get('mes', timezone.now().month))
    
    # Calcular primeiro e último dia do mês
    _, ultimo_dia_mes = monthrange(ano, mes)
    data_inicio_mes = timezone.datetime(ano, mes, 1).date()
    data_fim_mes = timezone.datetime(ano, mes, ultimo_dia_mes).date()
    
    # Buscar agendamentos do mês
    agendamentos = Agendamento.objects.filter(
        data_inicio__lte=data_fim_mes,
        data_fim__gte=data_inicio_mes
    ).order_by('data_inicio', 'hora_inicio')
    
    # Preparar dados do calendário
    primeiro_dia_semana = data_inicio_mes.weekday()  # 0=segunda, 6=domingo
    dias_mes_anterior = primeiro_dia_semana
    total_celulas = 42  # 6 semanas
    
    # Calcular mês anterior e próximo
    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano
        
    if mes == 12:
        mes_proximo = 1
        ano_proximo = ano + 1
    else:
        mes_proximo = mes + 1
        ano_proximo = ano
    
    # Obter último dia do mês anterior
    _, ultimo_dia_anterior = monthrange(ano_anterior, mes_anterior)
    
    # Construir grid do calendário
    dias_calendario = []
    
    # Dias do mês anterior
    for i in range(dias_mes_anterior):
        dia = ultimo_dia_anterior - dias_mes_anterior + i + 1
        dias_calendario.append({
            'dia': dia,
            'mes': mes_anterior,
            'ano': ano_anterior,
            'eh_mes_atual': False,
            'agendamentos': []
        })
    
    # Dias do mês atual
    for dia in range(1, ultimo_dia_mes + 1):
        data_dia = timezone.datetime(ano, mes, dia).date()
        agendamentos_dia = [
            ag for ag in agendamentos 
            if ag.data_inicio <= data_dia <= ag.data_fim
        ]
        
        dias_calendario.append({
            'dia': dia,
            'mes': mes,
            'ano': ano,
            'eh_mes_atual': True,
            'data': data_dia,
            'agendamentos': agendamentos_dia,
            'eh_hoje': data_dia == timezone.now().date()
        })
    
    # Dias do próximo mês
    dias_restantes = total_celulas - len(dias_calendario)
    for dia in range(1, dias_restantes + 1):
        dias_calendario.append({
            'dia': dia,
            'mes': mes_proximo,
            'ano': ano_proximo,
            'eh_mes_atual': False,
            'agendamentos': []
        })
    
    context = {
        'ano': ano,
        'mes': mes,
        'mes_nome': ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'][mes-1],
        'dias_calendario': dias_calendario,
        'mes_anterior': mes_anterior,
        'ano_anterior': ano_anterior,
        'mes_proximo': mes_proximo,
        'ano_proximo': ano_proximo,
        'hoje': timezone.now().date(),
        'salas': Sala.objects.filter(ativa=True),
    }
    
    return render(request, 'agendamento/calendario.html', context)

@login_required
def relatorios_agendamentos(request):
    """
    View principal de relatórios com filtros
    """
    # Filtros iniciais
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    sala_id = request.GET.get('sala')
    usuario_id = request.GET.get('usuario')
    
    # Query base
    agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
    # Aplicar filtros
    if data_inicio:
        agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_fim__lte=data_fim)
    if sala_id:
        agendamentos = agendamentos.filter(sala_id=sala_id)
    if usuario_id:
        agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
    # Estatísticas para o relatório
    total_agendamentos = agendamentos.count()
    salas_utilizadas = agendamentos.values('sala__nome').distinct().count()
    usuarios_ativos = agendamentos.values('usuario__username').distinct().count()
    
    # Calcular duração para cada agendamento
    for agendamento in agendamentos:
        diff = agendamento.data_fim - agendamento.data_inicio
        agendamento.duracao_dias = diff.days + 1
    
    context = {
        'agendamentos': agendamentos,
        'salas': Sala.objects.filter(ativa=True),
        'usuarios': User.objects.all(),
        'total_agendamentos': total_agendamentos,
        'salas_utilizadas': salas_utilizadas,
        'usuarios_ativos': usuarios_ativos,
        'filtros_aplicados': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'sala_id': sala_id,
            'usuario_id': usuario_id,
        }
    }
    
    return render(request, 'agendamento/relatorios.html', context)

@login_required
def exportar_pdf(request):
    """
    Exportar relatório para PDF usando xhtml2pdf
    """
    # Reutilizar a mesma lógica de filtros da view principal
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    sala_id = request.GET.get('sala')
    usuario_id = request.GET.get('usuario')
    
    agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
    if data_inicio:
        agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_fim__lte=data_fim)
    if sala_id:
        agendamentos = agendamentos.filter(sala_id=sala_id)
    if usuario_id:
        agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
    # Calcular estatísticas
    total_agendamentos = agendamentos.count()
    salas_utilizadas = agendamentos.values('sala__nome').distinct().count()
    
    for agendamento in agendamentos:
        diff = agendamento.data_fim - agendamento.data_inicio
        agendamento.duracao_dias = diff.days + 1
    
    context = {
        'agendamentos': agendamentos,
        'total_agendamentos': total_agendamentos,
        'salas_utilizadas': salas_utilizadas,
        'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'filtros_aplicados': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'sala_id': sala_id,
            'usuario_id': usuario_id,
        }
    }
    
    # Renderizar HTML para PDF
    html_string = render_to_string('agendamento/relatorio_pdf.html', context)
    
    # Gerar PDF com xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.pdf"'
    
    # Criar PDF
    pisa_status = pisa.CreatePDF(
        html_string,
        dest=response,
        encoding='UTF-8'
    )
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF: {}'.format(pisa_status.err))
    
    return response

@login_required
def exportar_excel(request):
    """
    Exportar relatório para Excel
    """
    # Reutilizar a mesma lógica de filtros
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    sala_id = request.GET.get('sala')
    usuario_id = request.GET.get('usuario')
    
    agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
    if data_inicio:
        agendamentos = agendamentos.filter(data_inicio__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_fim__lte=data_fim)
    if sala_id:
        agendamentos = agendamentos.filter(sala_id=sala_id)
    if usuario_id:
        agendamentos = agendamentos.filter(usuario_id=usuario_id)
    
    # Preparar dados para Excel
    dados = []
    for agendamento in agendamentos:
        diff = agendamento.data_fim - agendamento.data_inicio
        duracao_dias = diff.days + 1
        
        dados.append({
            'Sala': agendamento.sala.nome,
            'Usuário': agendamento.usuario.username,
            'Data Início': agendamento.data_inicio.strftime('%d/%m/%Y'),
            'Data Fim': agendamento.data_fim.strftime('%d/%m/%Y'),
            'Horário Início': agendamento.hora_inicio.strftime('%H:%M'),
            'Horário Fim': agendamento.hora_fim.strftime('%H:%M'),
            'Duração (dias)': duracao_dias,
            'Descrição': agendamento.descricao,
            'Data Criação': agendamento.data_criacao.strftime('%d/%m/%Y %H:%M'),
        })
    
    # Criar DataFrame e Excel
    df = pd.DataFrame(dados)
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Agendamentos', index=False)
                
                # Formatar a planilha
                worksheet = writer.sheets['Agendamentos']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Ler o arquivo temporário
            with open(tmp.name, 'rb') as f:
                excel_data = f.read()
    except Exception as e:
        return HttpResponse(f'Erro ao gerar Excel: {str(e)}')
    
    response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.xlsx"'
    
    return response

# Mantenha suas APIs existentes (api_dias_ocupados, api_verificar_disponibilidade)
# ... [suas APIs existentes] ...


def verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim, agendamento_id=None):
    """
    Verifica a disponibilidade de uma sala em um período específico
    Considera as regras especiais para Minhoto_Sonho, Minhoto e Sonho
    Retorna uma lista de datas com conflitos
    """
    conflitos = []
    current_date = data_inicio
    
    while current_date <= data_fim:
        # Determinar quais salas verificar baseado nas regras especiais
        if sala.nome == 'Minhoto_Sonho':
            # Para Minhoto_Sonho: verificar também Minhoto e Sonho
            salas_para_verificar = ['Minhoto_Sonho', 'Minhoto', 'Sonho']
        elif sala.nome in ['Minhoto', 'Sonho']:
            # Para salas individuais: verificar também Minhoto_Sonho
            salas_para_verificar = ['Minhoto_Sonho', sala.nome]
        else:
            # Para outras salas: apenas a própria sala
            salas_para_verificar = [sala.nome]
        
        # Verificar se há agendamentos conflitantes nesta data
        agendamentos_conflitantes = Agendamento.objects.filter(
            sala__nome__in=salas_para_verificar,
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
    Considera as regras especiais para Minhoto_Sonho, Minhoto e Sonho
    """
    _, ultimo_dia = monthrange(ano, mes)
    
    primeiro_dia_mes = timezone.datetime(ano, mes, 1).date()
    ultimo_dia_mes = timezone.datetime(ano, mes, ultimo_dia).date()
    
    # Buscar agendamentos que se sobrepõem com o mês
    if sala.nome == 'Minhoto_Sonho':
        # Para Minhoto_Sonho: também considerar ocupado quando Minhoto OU Sonho estiverem ocupadas
        agendamentos = Agendamento.objects.filter(
            data_inicio__lte=ultimo_dia_mes,
            data_fim__gte=primeiro_dia_mes
        ).filter(
            sala__nome__in=['Minhoto_Sonho', 'Minhoto', 'Sonho']
        )
    elif sala.nome in ['Minhoto', 'Sonho']:
        # Para salas individuais: também considerar ocupado quando Minhoto_Sonho estiver ocupada
        agendamentos = Agendamento.objects.filter(
            data_inicio__lte=ultimo_dia_mes,
            data_fim__gte=primeiro_dia_mes
        ).filter(
            sala__nome__in=['Minhoto_Sonho', sala.nome]
        )
    else:
        # Para outras salas: apenas agendamentos da própria sala
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

# Views principais
@login_required
def pagina_inicial(request):
    salas = Sala.objects.filter(ativa=True)
    meus_agendamentos = Agendamento.objects.filter(usuario=request.user).order_by('-data_inicio', '-hora_inicio')[:5]
    
    return render(request, 'agendamento/inicio.html', {
        'salas': salas,
        'meus_agendamentos': meus_agendamentos
    })

@login_required
def lista_salas(request):
    salas = Sala.objects.filter(ativa=True)
    
    # Paginação para salas
    page = request.GET.get('page', 1)
    paginator = Paginator(salas, 12)  # 12 salas por página
    
    try:
        salas_paginadas = paginator.page(page)
    except PageNotAnInteger:
        salas_paginadas = paginator.page(1)
    except EmptyPage:
        salas_paginadas = paginator.page(paginator.num_pages)
    
    # Estatísticas
    salas_ativas = salas.filter(ativa=True)
    salas_especiais = salas.filter(nome__in=['Minhoto', 'Sonho', 'Minhoto_Sonho'])
    
    return render(request, 'agendamento/lista_salas.html', {
        'salas': salas_paginadas,
        'salas_ativas': salas_ativas,
        'salas_especiais': salas_especiais,
    })

# @login_required
# def criar_agendamento(request, sala_id=None):
#     sala = None
#     if sala_id:
#         sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
#     if request.method == 'POST':
#         form = AgendamentoForm(request.POST)
#         if form.is_valid():
#             agendamento = form.save(commit=False)
#             agendamento.usuario = request.user
#             agendamento.save()
#             messages.success(request, 'Agendamento criado com sucesso!')
#             return redirect('pagina_inicial')
#         else:
#             messages.error(request, 'Por favor, corrija os erros abaixo.')
#     else:
#         initial = {'sala': sala} if sala else {}
#         form = AgendamentoForm(initial=initial)
    
#     salas = Sala.objects.filter(ativa=True)
#     return render(request, 'agendamento/criar_agendamento.html', {
#         'form': form,
#         'sala': sala,
#         'salas': salas
#     })

@login_required
def criar_agendamento(request, sala_id=None):
    sala = None
    if sala_id:
        sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
    # Obter parâmetros da URL
    data_selecionada = request.GET.get('data')
    hora_selecionada = request.GET.get('hora')
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            
            # Verificar disponibilidade antes de salvar
            conflitos = verificar_disponibilidade_sala(
                agendamento.sala,
                agendamento.data_inicio,
                agendamento.data_fim,
                agendamento.hora_inicio,
                agendamento.hora_fim
            )
            
            if conflitos:
                messages.error(request, f'Conflito de agendamento encontrado para esta sala.')
                for conflito in conflitos:
                    messages.error(request, f'Data {conflito["data"].strftime("%d/%m/%Y")} - {conflito["agendamento"].usuario.username}')
            else:
                agendamento.save()
                messages.success(request, 'Agendamento criado com sucesso!')
                return redirect('pagina_inicial')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Pré-preencher o formulário com dados da URL
        initial = {'sala': sala} if sala else {}
        
        # Se temos data e hora da URL, pré-preencher
        if data_selecionada and hora_selecionada:
            try:
                data_obj = timezone.datetime.strptime(data_selecionada, '%Y-%m-%d').date()
                hora_obj = timezone.datetime.strptime(hora_selecionada, '%H:%M').time()
                
                initial.update({
                    'data_inicio': data_obj,
                    'data_fim': data_obj,
                    'hora_inicio': hora_obj,
                    # Adicionar 1 hora como padrão para o fim
                    'hora_fim': (timezone.datetime.combine(data_obj, hora_obj) + timedelta(hours=1)).time()
                })
            except ValueError:
                # Se os parâmetros estiverem mal formatados, ignorar
                pass
        
        form = AgendamentoForm(initial=initial)
    
    salas = Sala.objects.filter(ativa=True)
    
    # Buscar disponibilidade para a sala selecionada (se houver)
    disponibilidade_info = None
    if sala and data_selecionada:
        try:
            data_obj = timezone.datetime.strptime(data_selecionada, '%Y-%m-%d').date()
            disponibilidade_info = {
                'sala': sala,
                'data': data_obj,
                'agendamentos': Agendamento.objects.filter(
                    sala=sala,
                    data_inicio__lte=data_obj,
                    data_fim__gte=data_obj
                ).order_by('hora_inicio')
            }
        except ValueError:
            disponibilidade_info = None
    
    return render(request, 'agendamento/criar_agendamento.html', {
        'form': form,
        'sala': sala,
        'salas': salas,
        'data_selecionada': data_selecionada,
        'hora_selecionada': hora_selecionada,
        'disponibilidade_info': disponibilidade_info
    })

@login_required
def meus_agendamentos(request):
    hoje = timezone.now().date()
    
    # AGORA MOSTRA TODOS OS AGENDAMENTOS, NÃO APENAS DO USUÁRIO LOGADO
    agendamentos = Agendamento.objects.all().order_by('-data_inicio', '-hora_inicio')
    
    # Paginação
    page = request.GET.get('page', 1)
    paginator = Paginator(agendamentos, 10)  # 10 agendamentos por página
    
    try:
        agendamentos_paginados = paginator.page(page)
    except PageNotAnInteger:
        agendamentos_paginados = paginator.page(1)
    except EmptyPage:
        agendamentos_paginados = paginator.page(paginator.num_pages)
    
    # Calcular estatísticas (usando queryset original)
    agendamentos_ativos = agendamentos.filter(data_fim__gte=hoje)
    agendamentos_futuros = agendamentos.filter(data_inicio__gt=hoje)
    agendamentos_passados = agendamentos.filter(data_fim__lt=hoje)
    
    # Obter lista de salas únicas que têm agendamentos
    salas_com_agendamentos = Sala.objects.filter(
        id__in=agendamentos.values_list('sala', flat=True).distinct()
    )
    
    # Calcular duração em dias para cada agendamento na página atual
    for agendamento in agendamentos_paginados:
        diff = agendamento.data_fim - agendamento.data_inicio
        agendamento.duracao_dias = diff.days + 1  # +1 para incluir o dia inicial
    
    return render(request, 'agendamento/meus_agendamentos.html', {
        'agendamentos': agendamentos_paginados,
        'agendamentos_ativos': agendamentos_ativos,
        'agendamentos_futuros': agendamentos_futuros,
        'agendamentos_passados': agendamentos_passados,
        'salas_com_agendamentos': salas_com_agendamentos,
        'hoje': hoje
    })


@login_required
def editar_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('meus_agendamentos')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = AgendamentoForm(instance=agendamento)
    
    return render(request, 'agendamento/editar_agendamento.html', {
        'form': form,
        'agendamento': agendamento
    })

@login_required
def excluir_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, usuario=request.user)
    
    if request.method == 'POST':
        agendamento.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
        return redirect('meus_agendamentos')
    
    return render(request, 'agendamento/excluir_agendamento.html', {
        'agendamento': agendamento
    })


@login_required
def disponibilidade_salas(request, data=None):
    """
    View para mostrar a disponibilidade de todas as salas em uma data específica
    COM REGRAS ESPECIAIS COMPLETAS PARA SALAS MINHOTO, SONHO E MINHOTO_SONHO
    """
    if not data:
        data = timezone.now().date()
    else:
        try:
            data = timezone.datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            data = timezone.now().date()
    
    # Buscar todos os agendamentos que cobrem a data especificada
    agendamentos = Agendamento.objects.filter(
        data_inicio__lte=data,
        data_fim__gte=data
    ).order_by('sala__nome', 'hora_inicio')
    
    # Organizar agendamentos por sala
    agendamentos_por_sala = {}
    for agendamento in agendamentos:
        if agendamento.sala.nome not in agendamentos_por_sala:
            agendamentos_por_sala[agendamento.sala.nome] = []
        agendamentos_por_sala[agendamento.sala.nome].append(agendamento)
    
    # Gerar horários do dia (das 06:00 às 22:00)
    horarios = []
    for hora in range(6, 22):
        for minuto in [0, 30]:
            horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Calcular disponibilidade
    salas = Sala.objects.filter(ativa=True)
    
    # Criar uma estrutura de dados mais simples para o template
    disponibilidade_simples = []
    
    for horario in horarios:
        hora_atual = timezone.datetime.strptime(horario, '%H:%M').time()
        linha = {'horario': horario, 'salas': []}
        
        # PRÉ-CALCULAR STATUS BASE DE TODAS AS SALAS
        status_base = {}
        agendamentos_base = {}
        
        for sala in salas:
            # Verificar se há conflito neste horário
            conflito = Agendamento.objects.filter(
                sala=sala,
                data_inicio__lte=data,
                data_fim__gte=data,
                hora_inicio__lte=hora_atual,
                hora_fim__gt=hora_atual
            ).first()
            
            if conflito:
                status_base[sala.nome] = 'ocupado'
                agendamentos_base[sala.nome] = conflito
            else:
                status_base[sala.nome] = 'livre'
                agendamentos_base[sala.nome] = None
        
        # APLICAR REGRAS ESPECIAIS BIDIRECIONAIS
        status_final = status_base.copy()
        agendamentos_final = agendamentos_base.copy()
        
        # Verificar status das salas especiais
        minhoto_status = status_base.get('Minhoto', 'livre')
        sonho_status = status_base.get('Sonho', 'livre') 
        minhoto_sonho_status = status_base.get('Minhoto_Sonho', 'livre')
        
        # REGRA 1: Se Minhoto OU Sonho estiver ocupada → Minhoto_Sonho fica indisponível
        if (minhoto_status == 'ocupado' or sonho_status == 'ocupado') and minhoto_sonho_status == 'livre':
            status_final['Minhoto_Sonho'] = 'indisponivel'
            # Usar o agendamento da sala que está causando a indisponibilidade
            if minhoto_status == 'ocupado':
                agendamentos_final['Minhoto_Sonho'] = agendamentos_base['Minhoto']
            else:
                agendamentos_final['Minhoto_Sonho'] = agendamentos_base['Sonho']
        
        # REGRA 2: Se Minhoto_Sonho estiver ocupada → Minhoto E Sonho ficam indisponíveis
        if minhoto_sonho_status == 'ocupado':
            if minhoto_status == 'livre':  # Só marca como indisponível se não estiver já ocupada
                status_final['Minhoto'] = 'indisponivel'
                agendamentos_final['Minhoto'] = agendamentos_base['Minhoto_Sonho']
            
            if sonho_status == 'livre':  # Só marca como indisponível se não estiver já ocupada
                status_final['Sonho'] = 'indisponivel'
                agendamentos_final['Sonho'] = agendamentos_base['Minhoto_Sonho']
        
        # CONSTRUIR LINHA FINAL COM STATUS APÓS REGRAS
        for sala in salas:
            status = status_final.get(sala.nome, 'livre')
            agendamento_conflitante = agendamentos_final.get(sala.nome)
            
            sala_info = {
                'nome': sala.nome,
                'status': status,
                'id': sala.id,
                'capacidade': sala.capacidade
            }
            
            if agendamento_conflitante:
                sala_info['agendamento'] = agendamento_conflitante
                
            linha['salas'].append(sala_info)
        
        disponibilidade_simples.append(linha)
    
    return render(request, 'agendamento/disponibilidade.html', {
        'data': data,
        'agendamentos_por_sala': agendamentos_por_sala,
        'disponibilidade_simples': disponibilidade_simples,
        'horarios': horarios,
        'salas': salas
    })

# APIs para o calendário
@login_required
def api_dias_ocupados(request, sala_id):
    """
    API que retorna os dias ocupados de uma sala para um mês específico
    """
    sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
    mes = int(request.GET.get('mes', datetime.now().month))
    ano = int(request.GET.get('ano', datetime.now().year))
    
    dias_ocupados = obter_dias_ocupados(sala, mes, ano)
    
    return JsonResponse({
        'sala_id': sala_id,
        'sala_nome': sala.nome,
        'mes': mes,
        'ano': ano,
        'dias_ocupados': dias_ocupados,
        'total_dias_ocupados': len(dias_ocupados)
    })

@login_required
def api_verificar_disponibilidade(request, sala_id):
    """
    API para verificar disponibilidade em tempo real
    """
    sala = get_object_or_404(Sala, id=sala_id, ativa=True)
    
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    hora_inicio = request.GET.get('hora_inicio')
    hora_fim = request.GET.get('hora_fim')
    
    if not all([data_inicio, data_fim, hora_inicio, hora_fim]):
        return JsonResponse({'error': 'Parâmetros incompletos'}, status=400)
    
    try:
        data_inicio = timezone.datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = timezone.datetime.strptime(data_fim, '%Y-%m-%d').date()
        hora_inicio = timezone.datetime.strptime(hora_inicio, '%H:%M').time()
        hora_fim = timezone.datetime.strptime(hora_fim, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Formato de data/hora inválido'}, status=400)
    
    conflitos = verificar_disponibilidade_sala(sala, data_inicio, data_fim, hora_inicio, hora_fim)
    
    return JsonResponse({
        'disponivel': len(conflitos) == 0,
        'total_conflitos': len(conflitos),
        'conflitos': [
            {
                'data': conflito['data'].strftime('%d/%m/%Y'),
                'responsavel': conflito['agendamento'].usuario.username,
                'horario': f"{conflito['agendamento'].hora_inicio.strftime('%H:%M')} - {conflito['agendamento'].hora_fim.strftime('%H:%M')}"
            }
            for conflito in conflitos
        ]
    })