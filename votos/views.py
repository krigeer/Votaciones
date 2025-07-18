from django.shortcuts import render, redirect   
from django.contrib import messages
from .forms import LoginForm
from .utils import validar_contrasena
from .models import Usuario, Password, Estado
import hashlib

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            contrasena = form.cleaned_data['contrasena']

        if not documento or not contrasena:
                messages.error(request, 'Los campos no pueden estar vacíos')
                return render(request, "login.html", {'form': form})
        else:
            password = contrasena
            validar_contrasena(password)
            if not validar_contrasena(password):
                messages.error(request, 'La contraseña no cumple con los requisitos')
                return render(request, "login.html", {'form': form})
            else:
                try:
                    usuario = Usuario.objects.get(numero_documento=documento)
                    password = Password.objects.filter(Usuario_id=usuario).latest('fecha_creacion')
                    md5= hashlib.md5(contrasena.encode()).hexdigest()
                    if password.password != md5:
                        messages.error(request, 'Contraseña incorrecta')
                        return render(request, "login.html", {'form': form})
                    if usuario.Estado.estado and usuario.Estado.estado.lower() == 'inactivo':
                        messages.error(request, 'Usuario inactivo')
                        return render(request, "login.htmll", {'form': form})
                    request.session['user_id'] = usuario.idUsuario
                    request.session['NombreUsuario'] = usuario.nombres_usuario 
                    request.session['is_authenticated'] = True

                    rol = usuario.rol.nombre.lower() if usuario.rol.nombre else None
                    if rol == 'gestor':
                        return redirect('appGestor:gestor')
                    elif rol == 'candidato':
                        return redirect('appCandidato:candidato')
                    elif rol == 'votante':
                        return redirect('appVotante:votante')
                    else:
                        messages.error(request, 'Permisos insuficientes')
                        return render(request, "login.html", {'form': form})
                except Usuario.DoesNotExist:
                    messages.error(request, 'Usuario no encontrado')
                    return render(request, "login.html", {'form': form})
                except Password.DoesNotExist:
                    messages.error(request, 'Contraseña no encontrada')
                    return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def gestor(request):
    return render(request, 'appGestor/panel.html')

def candidatos(request):
    return render(request, 'candidatos.html')