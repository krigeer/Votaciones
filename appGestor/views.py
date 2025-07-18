from django.shortcuts import render, redirect
from votos import models
# Create your views here.

def gestor(request):
    if not request.session.get('is_authenticated'):
        return redirect('votos:login')
    user_id = request.session.get('user_id')
    nombre_usuario = request.session.get('NombreUsuario')

    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
    }
    
    return render(request, 'appGestor/gestor.html', context)


