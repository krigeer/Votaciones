from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

#roles gestor, candidato, votante
class Roles(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
#programas del sena
class Programas(models.Model):
    idPrograma = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre

# fichas de los programas   
class Ficha(models.Model):
    idFicha = models.AutoField(primary_key=True)
    Programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    numeroFicha = models.BigIntegerField(unique=True)
    def __str__(self):
        return str(self.numeroFicha)

#estado activo, inactivo
class Estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.estado

#tipo de documento cedula, tarjeta de identidad, pasaporte
class TipoDocumento(models.Model):
    idTipoDocumento = models.AutoField(primary_key=True, unique=True)
    sigla = models.CharField(max_length=10, null=False, unique=True)
    descripcion = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.sigla

#usuarios   
class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    Estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    Ficha = models.ForeignKey(Ficha, on_delete=models.CASCADE)
    nombres_usuario = models.CharField(max_length=50, null=False)
    apellidos_usuario = models.CharField(max_length=50, null=False)
    idTipoDocumento = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    numero_documento = models.BigIntegerField(null=False, unique=True)
    email_usuario = models.EmailField(unique=True, null=False)
    numero_celular = models.BigIntegerField()
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.nombres_usuario

#contraseñas    
class Password(models.Model):
    idPassword = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    password = models.TextField(max_length=250, null=False)
    fecha_vencimiento = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.password
#Postulacion disponibles para los candidatos     
class Postulacion(models.Model):
    idPostulacion = models.AutoField(primary_key=True)
    nombre_postulacion = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre_postulacion
    
# fechas de votacion    
class FechaVotacion(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    motivo = models.ForeignKey(Postulacion, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.fecha_inicio.strftime('%d-%m-%Y %H:%M:%S') 



# cualidades de los candidatos
class Cualidad(models.Model):
    idCualidad = models.AutoField(primary_key=True)
    nombre_cualidad = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.nombre_cualidad    



# cada candidato tiene un usuario, una foto, una vacante, un estado y cuatro cualidades
class Candidato(models.Model):
    idCandidato = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    fin_postulacion = models.DateTimeField()
    foto = models.FileField(upload_to='foto_candidato', null=True, blank=True)
    vacante = models.ForeignKey(Postulacion, on_delete=models.CASCADE, null=True, blank=True)
    cualidades = models.ManyToManyField(Cualidad, related_name='candidatos', blank=True)

    @property
    def foto_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        return '/static/img/default-user.png'




# propuestas de los candidatos
class Propuesta(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, null=False)
    descripcion = models.TextField(max_length=400, null=False)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.titulo

# votos realizados por los votantes
class Voto(models.Model):
    votante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fecha_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('votante','candidato')  

    def __str__(self):
        return self.votante.nombres_usuario


