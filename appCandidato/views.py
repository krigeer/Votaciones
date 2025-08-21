from django.shortcuts import render, redirect
from votos.views import login
from votos.models import Usuario ,Candidato, Propuesta
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import Actualizar_foto, ActualizarPropuesta
from django.http import JsonResponse

# Create your views here.
def candidato(request):
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

    paginator = Paginator(candidatos, 5)  # 5 candidatos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
        'usuario': usuario,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'appCandidato/panel_candidato.html',context)



def registro_informacion(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')
    candidato = Candidato.objects.get(usuario=usuario)
    
   
    try:
        candidato = Candidato.objects.get(usuario=usuario)
    except Candidato.DoesNotExist:
        return JsonResponse({"success": False, "mensaje": "No existe candidato para este usuario."})

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if not form_type:
            return JsonResponse({"success": False, "mensaje": "No form type provided"})

        if form_type == 'form_foto':
            print("Formulario de foto recibido")
            form_foto = Actualizar_foto(request.POST, request.FILES, instance=candidato)
            if form_foto.is_valid():
                form_foto.save()
                return JsonResponse({"success": True, "mensaje": "Foto actualizada correctamente"})
            else:
                return JsonResponse({"success": False, "mensaje": form_foto.errors})
            
        elif form_type == 'form_propuesta':
                print("Formulario de propuesta recibido")
                form_propuesta = ActualizarPropuesta(request.POST, request.FILES)  # 👈 sin instance=candidato
                if form_propuesta.is_valid():
                    propuesta = form_propuesta.save(commit=False)  # 👈 aún no guarda
                    propuesta.candidato = candidato  # 👈 se asocia al candidato logueado
                    propuesta.save()  # 👈 ahora sí guarda en la BD
                    print("Propuesta guardada:", propuesta.titulo)
                    return JsonResponse({"success": True, "mensaje": "Propuesta registrada correctamente."})
                else:
                    print("Errores:", form_propuesta.errors)
                    return JsonResponse({"success": False, "mensaje": form_propuesta.errors})

    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
        'usuario': usuario,
        'form_foto': Actualizar_foto(instance=candidato),
        'form_propuesta': ActualizarPropuesta(instance=candidato),
    }

    return render(request, 'appCandidato/registro_informacion.html', context)