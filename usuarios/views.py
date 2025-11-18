from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout  # Adicione logout aqui
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('pagina_inicial')  # Nome simples
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redireciona para a URL em 'next' ou para a página inicial
            next_url = request.GET.get('next', 'pagina_inicial')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'usuarios/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('pagina_inicial')