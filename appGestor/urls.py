from django.urls import path
from . import views

app_name = 'appGestor'


urlpatterns = [
     path('gestor/', views.gestor, name='gestor'),
     path('importar-votantes/', views.importar_votantes, name='importar_votantes'),
]