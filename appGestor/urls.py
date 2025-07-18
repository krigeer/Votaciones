from django.urls import path
from . import views

app_name = 'appGestor'


urlpatterns = [
     path('gestor/', views.gestor, name='gestor'),
]