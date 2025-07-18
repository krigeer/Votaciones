from django.db import models

class Roles(models.Model):
    idRol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Programas(models.Model):
    idPrograma = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nombre
    
class Ficha(models.Model):
    idFicha = models.AutoField(primary_key=True)
    Programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    numeroFicha = models.BigIntegerField()
    def __str__(self):
        return self.numeroFicha

class Estado(models.Model):
    idEstado = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.estado

class TipoDocumento(models.Model):
    idTipoDocumento = models.AutoField(primary_key=True)
    sigla = models.CharField(max_length=10, null=False, unique=True)
    descripcion = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.sigla
    
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
    
class Password(models.Model):
    idPassword = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    password = models.TextField(max_length=50, null=False)
    fecha_vencimiento = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.password
    
class Candidato(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    foto = models.FileField(upload_to='foto_candidato', null=True, blank=True)

    def __str__(self):
        return f"Candidato: {self.usuario.nombres_usuario}"

class Propuesta(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50, null=False)
    descripcion = models.TextField(max_length=400, null=False)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.titulo

class Voto(models.Model):
    votante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    fecha_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('votante',)  # Un usuario solo puede votar una vez

    def __str__(self):
        return f"{self.votante.nombres_usuario} votó por {self.candidato.usuario.nombres_usuario}"
