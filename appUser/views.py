from django.shortcuts import render

# Create your views here.
def votante(request):
    if not request.session.get('is_authenticated'):
        messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
        return redirect('login')

    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    
    if usuario.rol.nombre.lower() != 'votante':
        messages.error(request, 'Acceso denegado. Solo los votantes pueden acceder a esta página.')
        return redirect('login')

    context = {
        'usuario': usuario
    }
    return render(request, 'appVotante/votante.html', context)