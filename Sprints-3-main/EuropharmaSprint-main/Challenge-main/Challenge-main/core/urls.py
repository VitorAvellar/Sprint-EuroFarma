from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', lambda request: redirect('login'), name='home'),
    path('index', views.index, name='index'),
    path('portal_admin', views.admin, name='portal_admin'),
    path('cadastro_geral', views.cadastro_geral, name='cadastro_geral'),
    path('acervo_videos', views.acervo_videos, name='acervo_videos'),
    path('deletar_video/<int:video_id>/', views.deletar_video, name='deletar_video'),
    path('login/', views.login_pagina, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('deletar_usuario/<int:usuario_id>/', views.deletar_usuario, name='deletar_usuario'),
    path('listar_usuario/', views.listar_usuario, name='listar_usuario'),
    path('faq/', views.faq, name='faq'),
    path('cadastro_pergunta/', views.cadastro_pergunta, name='cadastro_pergunta'),
    path('deletar_pergunta/<int:pergunta_id>/', views.deletar_pergunta, name='deletar_pergunta'),
    path('adicionar_video', views.adicionar_video, name='adicionar_video'),
    path('cadastrar_setores/', views.cadastrar_setores, name='cadastrar_setores'),
    path('cadastrar_modulos/', views.cadastrar_modulos, name='cadastrar_modulos'),
    path('cadastro_material/', views.cadastro_material, name='cadastro_material'),
    path('listar_material/', views.listar_material, name='listar_material'),
    path('download/<int:material_id>/', views.download_document, name='download_document'),
    path('deletar_material/<int:material_id>/', views.deletar_material, name='deletar_material'),
    path('listar_setores/', views.listar_setores, name='listar_setores'),
    path('deletar_setor/<int:setor_id>/', views.deletar_setor, name='deletar_setor'),
    path('listar_modulos/', views.listar_modulos, name='listar_modulos'),
    path('modulos/deletar/<int:modulo_id>/', views.deletar_modulo, name='deletar_modulo'),
    path('cadastrar_exercicio/', views.cadastrar_exercicio, name='cadastrar_exercicio'),
    path('cadastrar_treinamento/', views.cadastrar_treinamento, name='cadastrar_treinamento'),
    path('listar_treinamento/', views.listar_treinamento, name='listar_treinamento'),
    path('deletar_treinamento/<int:treinamento_id>/', views.deletar_treinamento, name='deletar_treinamento'),
    path('cadastrar_exercicio/', views.cadastrar_exercicio, name='cadastrar_exercicio'),
    path('listar_exercicios/', views.listar_exercicios, name='listar_exercicios'),
    path('deletar_exercicio/<int:exercicio_id>/', views.deletar_exercicio, name='deletar_exercicio'),
    # path('questionario/', views.questionario, name='questionario'),
]