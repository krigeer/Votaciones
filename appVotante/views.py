from django.shortcuts import render, redirect
from votos.views import login
from votos.models import Usuario, Candidato, Propuesta
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def votante_view(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')
    query = request.GET.get('q', '')

    candidatos = Candidato.objects.select_related('usuario').prefetch_related('propuesta_set')
    if query:
        candidatos = candidatos.filter(
            Q(usuario__nombres_usuario__icontains=query) |
            Q(usuario__apellidos_usuario__icontains=query)
        )

    # Paginación
    paginator = Paginator(candidatos, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
        'usuario': usuario,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'appVotante/panel_votante.html', context)


