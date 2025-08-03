from django.urls import path
from .views import votante_view

app_name = 'appVotante'
urlpatterns = [
    path('votante/', votante_view, name='votantes'),
]