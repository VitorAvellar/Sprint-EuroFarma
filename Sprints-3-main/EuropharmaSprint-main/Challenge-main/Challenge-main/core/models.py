from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Setores(models.Model):
    nome_setor = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_setor

class Clientes(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cliente", null=True)
    nome = models.CharField(max_length=255)
    setor = models.ForeignKey(Setores, on_delete=models.SET_NULL, null=True)
    data_de_nascimento = models.DateField(null=True)
    data_inscricao = models.DateTimeField(default=timezone.now)
    email = models.EmailField()

class Treinamentos(models.Model):
    nome_treinamento = models.CharField(max_length=255)
    setor = models.ForeignKey(Setores, on_delete=models.SET_NULL, null=True)

class AcervoVideos(models.Model):
    nome_video = models.CharField(max_length=255)
    descricao = models.TextField()
    url_video = models.URLField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    treinamento = models.ForeignKey(Treinamentos, on_delete=models.SET_NULL, null=True)

class TipoPergunta(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo

class Pergunta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_pergunta = models.ForeignKey('TipoPergunta', on_delete=models.SET_NULL, null=True)
    texto_pergunta = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.texto_pergunta

class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    texto_resposta = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Torna opcional
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.texto_resposta

