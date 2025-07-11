from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('gestor/', views.gestor, name='gestor'),
    path('candidatos/', views.candidatos, name='candidatos')
]
