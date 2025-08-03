from django.urls import path
from . import views

app_name = 'appGestor'

urlpatterns = [
     path('gestor/', views.gestor, name='gestor'),
     path('importar-votantes/', views.importar_votantes, name='importar_votantes'),
     path('buscar_usuario/', views.buscar_usuario, name='buscar_usuario'),
     path('votantes/', views.votante, name='votantes'),
     path('admins/', views.admins, name='admins'),
     path('candidatos/', views.candidatos, name='candidatos'),
     path('enviar-mensaje/', views.enviar_mensaje_masivo, name='enviar_mensaje_masivo'),
     # path('anadir_candidato/', views.anadir_candidato, name='anadir_candidato'), (pruebas)
     path('volver-candidato/', views.volver_candidato, name='volver_candidato'),
]