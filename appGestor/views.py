from django.shortcuts import render, redirect
from .forms import FechaVotacionForm, UsuarioForm, NuevoCandidatoForm
from votos.models import FechaVotacion, Usuario, Voto, Password ,TipoDocumento, Estado, Ficha, Roles, Candidato, Propuesta
from django.utils import timezone
from django.http import JsonResponse
import string ,hashlib, random, openpyxl, pandas as pd
from datetime import date, timedelta
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from votos.utils import generar_password
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mass_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from votos.views import login

# Create your views here.


def gestor(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')
    
    ultima_fecha = FechaVotacion.objects.order_by('-id').first()
    if ultima_fecha and ultima_fecha.fecha_fin:
        ahora = timezone.now().date()  
        fecha_fin = ultima_fecha.fecha_fin.date()  
        diferencia = fecha_fin - ahora  
    if diferencia.days >= 0:
        tiempo_restante = f'{diferencia.days} días'
    else:
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        tiempo_restante = f"{horas} horas y {minutos} minutos."

    votantes = Usuario.objects.filter(rol_id=3).count()
    candidatos = Usuario.objects.filter(rol_id=2).count()
    votos = Voto.objects.filter(fecha_voto__lte=ultima_fecha.fecha_fin).count()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'usuario':
            usuarioForm = UsuarioForm(request.POST)
            if usuarioForm.is_valid():
                numero_documento = usuarioForm.cleaned_data['numero_documento']
                if Usuario.objects.filter(numero_documento=numero_documento).exists():
                    return JsonResponse({'error': False, 'error': 'El número de documento ya está registrado.'})
                else:
                    usuario = usuarioForm.save()


                    random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                    hashed_password = hashlib.md5(random_password.encode()).hexdigest()
                    Password.objects.create(
                        Usuario=usuario,
                        password=hashed_password,
                        fecha_creacion=date.today(),
                        fecha_vencimiento=date.today() + timedelta(days=90)
                    )
                    html_content = render_to_string('correos/contrasena.html', {
                        'nombre': usuario.nombres_usuario,
                        'correo': usuario.email_usuario,
                        'contrasena': random_password,
                    })

                    email = EmailMultiAlternatives(
                        subject='Bienvenido al Sistema de Inventario',
                        body='Este correo requiere un visor HTML.',
                        from_email='inventariosena01@gmail.com',  
                        to=[usuario.email_usuario],
                        )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': usuarioForm.errors})

        elif form_type == 'fecha':
            fechaVotacion = FechaVotacionForm(request.POST)
            if fechaVotacion.is_valid():
                fechaVotacion.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errors': fechaVotacion.errors})

        else:
            return JsonResponse({'success': False, 'text': 'Datos faltantes'})

                            
                    

    usuarioForm = UsuarioForm()
    fechaVotacion = FechaVotacionForm()
    todos_usuarios = Usuario.objects.all().order_by('nombres_usuario')
    roles = Roles.objects.all()

    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
        'FechaVotacion': fechaVotacion,
        'ultima_fecha': ultima_fecha,
        'tiempo_restante': tiempo_restante,
        'votantes': votantes,
        'candidatos': candidatos,
        'votos': votos,
        'usuarioForm': usuarioForm,
        'todos_usuarios': todos_usuarios,
        'roles': roles,
        'usuario': usuario,
        
    }

    return render(request, 'appGestor/gestor.html', context)


@csrf_exempt
def importar_votantes(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    nombre_usuario = request.session.get('NombreUsuario')

    ultima_fecha = FechaVotacion.objects.order_by('-id').first()
    if ultima_fecha and ultima_fecha.fecha_fin:
        ahora = timezone.now().date()  
        fecha_fin = ultima_fecha.fecha_fin.date()  
        diferencia = fecha_fin - ahora  
    if diferencia.days >= 0:
        tiempo_restante = f'{diferencia.days} días'
    else:
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        tiempo_restante = f"{horas} horas y {minutos} minutos."

    votantes = Usuario.objects.filter(rol_id=3).count()
    candidatos = Usuario.objects.filter(rol_id=2).count()
    votos = Voto.objects.filter(fecha_voto__lte=ultima_fecha.fecha_fin).count()

    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        df = pd.read_excel(archivo)

        creados = 0
        existentes = 0
        errores = 0

        for _, row in df.iterrows():
            try:
                tipo_doc = TipoDocumento.objects.get(sigla=row['tipo_documento'])
                ficha = Ficha.objects.get(numeroFicha=row['ficha'])
                estado = Estado.objects.get(estado=row['estado'])
                rol = Roles.objects.get(nombre=row['rol'])

                usuario, creado = Usuario.objects.get_or_create(
                    numero_documento=row['numero_documento'],
                    defaults={
                        'nombres_usuario': row['nombres_usuario'],
                        'apellidos_usuario': row['apellidos_usuario'],
                        'idTipoDocumento': tipo_doc,
                        'email_usuario': row['email_usuario'],
                        'numero_celular': row['numero_celular'],
                        'Ficha': ficha,
                        'Estado': estado,
                        'rol': rol
                    }
                )

                if creado:
                    random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                    hashed_password = hashlib.md5(random_password.encode()).hexdigest()
                    
                    Password.objects.create(
                        Usuario=usuario,
                        password=hashed_password,
                        fecha_creacion=date.today(),
                        fecha_vencimiento=date.today() + timedelta(days=90)
                    )

                    html_content = render_to_string('correos/contrasena.html', {
                        'nombre': usuario.nombres_usuario,
                        'correo': usuario.email_usuario,
                        'contrasena': random_password,
                    })

                    email = EmailMultiAlternatives(
                        subject='Bienvenido al Sistema de Votaciones',
                        body='Este correo requiere un visor HTML.',
                        from_email='inventariosena01@gmail.com',
                        to=[usuario.email_usuario],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    creados += 1
                else:
                    existentes += 1

            except Exception as e:
                print(f'Error importando {row.get("email_usuario", "Desconocido")}: {e}')
                errores += 1

        messages.success(request, f'Importación finalizada. Nuevos: {creados}, Existentes: {existentes}, Errores: {errores}')
        return redirect('appGestor:importar_votantes')
    
    context = {
        'user_id': user_id,
        'nombre_usuario': nombre_usuario,
        'ultima_fecha': ultima_fecha,
        'tiempo_restante': tiempo_restante,
        'votantes': votantes,
        'candidatos': candidatos,
        'votos': votos,
    }


    return render(request, 'appGestor/importar_votantes.html', context)








def buscar_usuario(request):
    numero_documento = request.GET.get('numero_documento')
    try:
        usuario = Usuario.objects.get(numero_documento=numero_documento)
        return JsonResponse({
            'success': True,
            'usuario': {
                'id': usuario.idUsuario,
                'nombres_usuario': usuario.nombres_usuario,
                'apellidos_usuario': usuario.apellidos_usuario,
                'numero_documento': usuario.numero_documento,
                'email_usuario': usuario.email_usuario,
                'rol_nombre': usuario.rol.nombre,
            }
        })
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False})
    

def votante(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')
    
    query = request.GET.get('q', '')

    votantes_lista = Usuario.objects.filter(rol_id=3).order_by('idUsuario')

    if query:
        votantes_lista = votantes_lista.filter(
            Q(nombres_usuario__icontains=query) | Q(numero_documento__icontains=query)
        )

    votantes_lista = votantes_lista.order_by('idUsuario')

    paginator = Paginator(votantes_lista, 50)
    page = request.GET.get('page')

    try:
        votantes = paginator.page(page)
    except PageNotAnInteger:
        votantes = paginator.page(1)
    except EmptyPage:
        votantes = paginator.page(paginator.num_pages)

    context = {
        'usuario': usuario,
        'nombre_usuario': nombre_usuario,
        'votantes': votantes,
        'query': query,
    }
    return render(request, 'appGestor/votantes.html', context)


def admins(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')

    query = request.GET.get('q', '')

    gestor_lista = Usuario.objects.filter(rol_id=1).order_by('idUsuario')

    if query:
        gestor_lista = gestor_lista.filter(
            Q(nombres_usuario__icontains=query) | Q(numero_documento__icontains=query)
        )

    gestor_lista = gestor_lista.order_by('idUsuario')
    

  
    paginator = Paginator(gestor_lista, 10)
    page = request.GET.get('page')

    try:
        gestor = paginator.page(page)
    except PageNotAnInteger:
        gestor = paginator.page(1)
    except EmptyPage:
        gestor = paginator.page(paginator.num_pages)

    context = {
        'usuario': usuario,
        'nombre_usuario': nombre_usuario,
        'gestor': gestor,
        'query': query,
    }
    return render(request, 'appGestor/admins.html', context)


def candidatos(request):
    if not request.session.get('is_authenticated'):
        return redirect(login)
    
    user_id = request.session.get('user_id')
    usuario = Usuario.objects.get(idUsuario=user_id)
    nombre_usuario = request.session.get('NombreUsuario')

    query = request.GET.get('q', '')
 
    candidatos_lista = Usuario.objects.filter(rol_id=2)
    
    if query:
        candidatos_lista = candidatos_lista.filter(
            Q(nombres_usuario__icontains=query) | Q(numero_documento__icontains=query)
        )

    candidatos_lista = candidatos_lista.order_by('idUsuario')

   
    paginator = Paginator(candidatos_lista, 10)
    page = request.GET.get('page')

    try:
        candidato = paginator.page(page)
    except PageNotAnInteger:
        candidato = paginator.page(1)
    except EmptyPage:
        candidato = paginator.page(paginator.num_pages)

    context = {
        'usuario': usuario,
        'nombre_usuario': nombre_usuario,
        'candidato': candidato,
        'query': query,
    }
    return render(request, 'appGestor/candidatos.html', context)


def enviar_mensaje_masivo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje')

            if not mensaje:
                return JsonResponse({'ok': False, 'error': 'Mensaje vacío'})

            from votos.models import Usuario
            usuarios = Usuario.objects.all()

            subject = "Mensaje del sistema"
            from_email = 'inventariosena01@gmail.com'  

            enviados = 0
            fallidos = []

            for usuario in usuarios:
                try:
                    html_content = render_to_string('correos/mensaje.html', {
                        'nombre': usuario.nombres_usuario,
                        'correo': usuario.email_usuario,
                        'mensaje': mensaje
                    })

                    email = EmailMultiAlternatives(
                        subject=subject,
                        body='Este correo requiere un visor HTML.',
                        from_email=from_email,
                        to=[usuario.email_usuario],
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    enviados += 1
                except Exception as e:
                    fallidos.append({'correo': usuario.email_usuario, 'error': str(e)})

            return JsonResponse({
                'ok': True,
                'enviados': enviados,
                'fallidos': fallidos,
                'total': usuarios.count()
            })

        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})

    return JsonResponse({'ok': False, 'error': 'Método no permitido'})


def volver_candidato(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            id_usuario = data.get("idUsuario")
            
            usuario = Usuario.objects.get(idUsuario=id_usuario)
            
            usuario.rol_id = 2
            
            Candidato.objects.create(usuario=usuario)
            usuario.save()

            return JsonResponse({"ok": True, "mensaje": "Usuario convertido en candidato."})
        except Usuario.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Usuario no encontrado."})
        except Exception as e:
            return JsonResponse({"ok": False, "error": f"Error interno: {str(e)}"})

    return JsonResponse({"ok": False, "error": "Método no permitido"}, status=405)