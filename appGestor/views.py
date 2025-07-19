from django.shortcuts import render, redirect
from .forms import FechaVotacionForm, UsuarioForm, OtroFormulario 
from votos.models import FechaVotacion, Usuario, Voto, Password ,TipoDocumento, Estado, Ficha, Roles
from django.utils import timezone
from django.http import JsonResponse
import string ,hashlib, random, openpyxl, pandas as pd
from datetime import date, timedelta
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from votos.utils import generar_password
from django.contrib import messages
# Create your views here.


def gestor(request):
    if not request.session.get('is_authenticated'):
        return redirect('votos:login')
    
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

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'usuario':
            print(request.POST)
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
            print(request.POST)
            fechaVotacion = FechaVotacionForm(request.POST)
            if fechaVotacion.is_valid():
                fechaVotacion.save()
                return JsonResponse({'success': True})
        
        # Agrega aquí más formularios según los necesites

        return JsonResponse({'success': False, 'error': 'Formulario inválido'})

    usuarioForm = UsuarioForm()
    fechaVotacion = FechaVotacionForm()

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
    }

    return render(request, 'appGestor/gestor.html', context)


@csrf_exempt
def importar_votantes(request):
    if not request.session.get('is_authenticated'):
        return redirect('votos:login')
    
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