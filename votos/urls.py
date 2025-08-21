from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='inicio'),
    path('login/', views.login, name='login'),
    path('', include('appGestor.urls')),
    path('todos_candidatos/', views.candidatos, name='todos_candidatos'),
    path('logout/', views.logout_view, name='logout'),
    path('detalles_candidato/<int:idCandidato>/', views.detalles_candidato, name='detalles_candidato'),
    path('', include('appVotante.urls')),
    path('', include('appCandidato.urls')),
]
