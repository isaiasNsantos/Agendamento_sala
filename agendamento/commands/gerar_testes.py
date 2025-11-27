# sua_app/management/commands/gerar_testes.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from agendamento.models import Sala, Agendamento
from datetime import datetime, timedelta
import random
from django.utils import timezone

class Command(BaseCommand):
    help = 'Gera agendamentos de teste para o sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--quantidade',
            type=int,
            default=10,
            help='Número de agendamentos a serem criados (padrão: 10)',
        )

    def handle(self, *args, **options):
        quantidade = options['quantidade']
        
        salas = Sala.objects.all()
        usuarios = User.objects.all()
        
        if not salas:
            self.stdout.write(
                self.style.ERROR('❌ Nenhuma sala encontrada. Crie salas primeiro.')
            )
            return
            
        if not usuarios:
            self.stdout.write(
                self.style.ERROR('❌ Nenhum usuário encontrado. Crie usuários primeiro.')
            )
            return
        
        descricoes = [
            "Reunião de equipe - Desenvolvimento de novos projetos",
            "Treinamento de boas práticas - Sala de treinamento",
            "Apresentação comercial para parceiros estratégicos",
            "Workshop de inovação e criatividade",
            "Revisão de desempenho trimestral",
            "Capacitação em ferramentas digitais",
            "Demonstração de protótipos para stakeholders",
            "Sessão de planejamento estratégico",
            "Formação de novas lideranças",
            "Brainstorming para campanhas de marketing",
            "Análise de resultados e métricas",
            "Oficina de resolução de problemas",
            "Preparação para auditoria interna",
            "Dinâmica de integração de novos membros",
            "Reunião de alinhamento departamental"
        ]
        
        agendamentos_criados = 0
        
        for i in range(quantidade):
            try:
                sala = random.choice(salas)
                usuario = random.choice(usuarios)
                
                data_hoje = timezone.now().date()
                data_inicio = data_hoje + timedelta(days=random.randint(0, 30))
                
                if random.random() < 0.7:
                    data_fim = data_inicio
                else:
                    data_fim = data_inicio + timedelta(days=random.randint(1, 3))
                
                # Horário comercial
                hora_inicio = timedelta(
                    hours=random.randint(8, 16),
                    minutes=random.choice([0, 30])
                )
                
                duracao_horas = random.randint(1, 4)
                hora_fim = hora_inicio + timedelta(hours=duracao_horas)
                
                descricao = random.choice(descricoes)
                
                agendamento = Agendamento(
                    sala=sala,
                    usuario=usuario,
                    data_inicio=data_inicio,
                    data_fim=data_fim,
                    hora_inicio=(datetime.min + hora_inicio).time(),
                    hora_fim=(datetime.min + hora_fim).time(),
                    descricao=f"{descricao} [TESTE {i+1}]",
                    data_criacao=timezone.now()
                )
                
                agendamento.save()
                agendamentos_criados += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Agendamento {i+1} criado com sucesso!')
                )
                self.stdout.write(f'   🏢 Sala: {sala.nome}')
                self.stdout.write(f'   👤 Usuário: {usuario.username}')
                self.stdout.write(f'   📅 Período: {data_inicio} a {data_fim}')
                self.stdout.write(f'   🕐 Horário: {agendamento.hora_inicio} - {agendamento.hora_fim}')
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erro ao criar agendamento {i+1}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Total de agendamentos de teste criados: {agendamentos_criados}/{quantidade}'
            )
        )