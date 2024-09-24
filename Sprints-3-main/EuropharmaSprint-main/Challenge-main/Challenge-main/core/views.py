from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import ClienteForm, PerguntaForm, RespostaForm
from .models import AcervoVideos, Pergunta, Resposta


def index(request):
    return render(request, 'core/index.html')

def admin(request):
    return render(request, 'core/portal_admin.html')

def cadastro_geral(request):
    return render(request, 'core/cadastro_geral.html')

def acervo_videos(request):
    lista_videos = [
        'https://www.youtube.com/watch?v=BPnaXaEq_Hg&list=PLONqVfazBqhWMeuAmfn-5znJ1tamV8jGc&index=2',
        'https://www.youtube.com/watch?v=fFuTkavmsxo&list=PLONqVfazBqhWMeuAmfn-5znJ1tamV8jGc&index=3',
        'https://www.youtube.com/watch?v=AGdSBSVMYR8&list=PLONqVfazBqhWMeuAmfn-5znJ1tamV8jGc&index=4',
        'https://www.youtube.com/watch?v=ffGd7biISFg&list=PLONqVfazBqhWMeuAmfn-5znJ1tamV8jGc&index=5',
        'https://www.youtube.com/watch?v=JU823WoH3W8',
        'https://www.youtube.com/watch?v=PI3GopnvQ54',
        'https://www.youtube.com/watch?v=Ie4S6Qxi6do'
    ]

    context = {
        'videos': lista_videos,
    }

    return render(request, 'core/acervo_videos.html', context)


def login(request):
    return render(request, 'login.html')

def cadastro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../login')
    else:
        form = ClienteForm()

    return render(request, "core/cadastro_cliente.html", {'form': form})

def login_pagina(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../index')
        else:
            return render(request, 'core/login.html', {'error': 'Login inválido.'})
    else:
        return render(request, 'core/login.html')


def ger_treinamento(request):
    acervo_videos = AcervoVideos.objects.all()
    return render(request, 'ger_treinamento.html', {'acervo_videos': acervo_videos})


def cadastro_usuario(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = ClienteForm()
    return render(request, 'core/cadastro_usuario.html', {'form': form})

def listar_usuario(request):
    usuarios = User.objects.all()  # Obtém todos os usuários
    return render(request, 'core/listar_usuario.html', {'usuarios': usuarios})

def cadastro_pergunta(request):
    if request.method == 'POST':
        form = PerguntaForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            usuario = User.objects.get(username=username)  
            pergunta = form.save(commit=False)
            pergunta.usuario = usuario  
            pergunta.save()
            return redirect('faq')  
    else:
        form = PerguntaForm()

    return render(request, 'core/cadastro_pergunta.html', {'form': form})


def faq(request):
    query = request.GET.get('q')
    
    if query:
        # Filtra perguntas que têm um usuário associado e cujo nome de usuário contém a consulta
        perguntas = Pergunta.objects.filter(usuario__username__icontains=query).exclude(usuario__isnull=True)
    else:
        perguntas = Pergunta.objects.all()
    
    if request.method == 'POST':
        pergunta_id = request.POST.get('pergunta_id')
        pergunta = get_object_or_404(Pergunta, id=pergunta_id)
        form = RespostaForm(request.POST)
        
        if form.is_valid():
            resposta = form.save(commit=False)
            resposta.pergunta = pergunta
            resposta.save()  # Salva a resposta sem associar a um usuário
            return redirect('faq')
    else:
        form = RespostaForm()

    return render(request, 'core/faq.html', {'perguntas': perguntas, 'form': form})