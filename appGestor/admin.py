from django.contrib import admin
from votos.models import Roles, Programas, Ficha, Estado, TipoDocumento, Usuario, Password, Candidato, Propuesta, Voto, FechaVotacion, Postulacion, Cualidad

admin.site.register(Roles)
admin.site.register(Programas)
admin.site.register(Ficha)
admin.site.register(Estado)
admin.site.register(TipoDocumento)
admin.site.register(Usuario)
admin.site.register(Password)
admin.site.register(Candidato)
admin.site.register(Propuesta)
admin.site.register(Voto)
admin.site.register(FechaVotacion)
admin.site.register(Postulacion)
admin.site.register(Cualidad)

