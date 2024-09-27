from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import ClienteForm, MaterialForm, PerguntaForm, RespostaForm, AcervoVideoForm, SetorForm, ModuloForm
from .models import AcervoVideos, Pergunta, Resposta, Setores, Modulos, Material
from django.http import HttpResponse, Http404
import mimetypes


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

def acervo_videos(request):
    # Obtenha o valor do setor filtrado da URL (se houver)
    setor_id = request.GET.get('setor')

    if setor_id:
        # Se um setor foi selecionado, filtre os vídeos por esse setor
        videos = AcervoVideos.objects.filter(setor_id=setor_id)
    else:
        # Caso contrário, exiba todos os vídeos
        videos = AcervoVideos.objects.all()

    # Pega todos os setores para popular o dropdown
    setores = Setores.objects.all()

    # Renderiza o template com os vídeos e os setores disponíveis para filtro
    return render(request, 'core/acervo_videos.html', {'videos': videos, 'setores': setores})

def adicionar_video(request):
    if request.method == 'POST':
        form = AcervoVideoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o vídeo no banco de dados
            return redirect('acervo_videos')
    else:
        form = AcervoVideoForm()

    return render(request, 'core/adicionar_video.html', {'form': form})

def cadastrar_setores(request):
    if request.method == 'POST':
        form = SetorForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo setor no banco de dados
            return redirect('cadastrar_setores')
    else:
        form = SetorForm()
    
    return render(request, 'core/cadastrar_setores.html', {'form': form})

def deletar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()  
    return redirect('listar_usuario')  

def deletar_video(request, video_id):
    video = get_object_or_404(AcervoVideos, id=video_id)
    video.delete()  # Exclui o vídeo do banco de dados
    return redirect('acervo_videos')  # Redireciona para a lista de vídeos


def deletar_pergunta(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, id=pergunta_id)
    pergunta.delete()  # Exclui a pergunta do banco de dados
    return redirect('faq')  # Redireciona para a lista de perguntas no FAQ

def cadastrar_modulos(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo módulo no banco de dados
            return redirect('cadastrar_modulos')
    else:
        form = ModuloForm()
    
    return render(request, 'core/cadastrar_modulos.html', {'form': form})

# Metodo responsavel por realizar o upload e cadastro dos arquivo
def cadastro_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_material')
    else:
        form = MaterialForm()
    
    return render(request, 'core/cadastro_material.html', {'form': form})

# Metodo responsavel por Listar o arquivo
def listar_material(request):
    # Obtém o valor do módulo filtrado da URL (se houver)
    modulo_id = request.GET.get('modulo')

    if modulo_id:
        # Se um módulo foi selecionado, filtre os materiais por esse módulo
        material = Material.objects.filter(modulo_id=modulo_id).select_related('modulo')
    else:
        # Caso contrário, exiba todos os materiais
        material = Material.objects.all().select_related('modulo')

    # Pega todos os módulos para popular o dropdown
    modulos = Modulos.objects.all()

    return render(request, 'core/listar_material.html', {'material': material, 'modulos': modulos})

# Metodo responsavel por realizar o download dos arquivo
def download_document(request, material_id):
    try:
        material = Material.objects.get(id=material_id)

    # Utilizando o import da  mimetypes com o objetivo de identificar automaticamente qual a exteção do arquivo
        file_path = material.file.path
        content_type, encoding = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = 'application/octet-stream'  # Tipo genérico para arquivos binários

        # Informando ao HTTP qual o tipo do arquivo que ira ser armazenado
        response = HttpResponse(material.file, content_type=content_type )  
        response['Content-Disposition'] = f'attachment; filename="{material.file.name}"'
        return response 
    except material.DoesNotExist:
        raise Http404("Documento não encontrado.")
    
def deletar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    
    if request.method == 'POST':
        material.delete()
        return redirect('listar_material')  # Redireciona para a página de listagem após a exclusão
    
    # return render(request, 'confirm_delete.html', {'material': material})
 

def listar_setores(request):
    setores = Setores.objects.all()  # Obtém todos os setores cadastrados
    return render(request, 'core/listar_setores.html', {'setores': setores})

def deletar_setor(request, setor_id):
    setor = get_object_or_404(Setores, id=setor_id)
    setor.delete()  # Deleta o setor do banco de dados
    return redirect('listar_setores')  # Redireciona para a página de listagem dos setores