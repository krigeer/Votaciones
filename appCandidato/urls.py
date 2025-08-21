from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'appCandidato'
urlpatterns = [
    path('candidato/', views.candidato, name='candidato'),
    path('registro_informacion/', views.registro_informacion, name='registro_informacion'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)