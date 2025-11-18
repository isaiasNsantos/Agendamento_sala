# Sistema de Agendamento de Salas - RH

Sistema Django para gerenciamento e agendamento de salas de reunião.

## Funcionalidades

- Agendamento de salas
- Calendário de disponibilidade
- Relatórios administrativos
- Exportação PDF/Excel
- Controle de permissões

## Tecnologias

- Django 4.x
- Python 3.x
- Bootstrap
- SQLite

## Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente: `venv\Scripts\activate` (Windows)
4. Instale dependências: `pip install -r requirements.txt`
5. Execute migrações: `python manage.py migrate`
6. Crie superusuário: `python manage.py createsuperuser`
7. Execute: `python manage.py runserver`