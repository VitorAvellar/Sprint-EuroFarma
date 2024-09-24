from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('portal_admin', views.admin, name='portal_admin'),
    path('cadastro_geral', views.cadastro_geral, name='cadastro_geral'),
    path('acervo_videos', views.acervo_videos, name='acervo_videos'),
    path('login/', views.login_pagina, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('cadastro_usuario/', views.cadastro_usuario, name='cadastro_usuario'),
    path('listar_usuario/', views.listar_usuario, name='listar_usuario'),
    path('faq/', views.faq, name='faq'),
    path('cadastro_pergunta/', views.cadastro_pergunta, name='cadastro_pergunta'),
]