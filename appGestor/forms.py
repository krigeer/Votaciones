from django import forms
from votos.models import FechaVotacion, Usuario

class FechaVotacionForm(forms.ModelForm):
    class Meta:
        model = FechaVotacion
        fields = ['fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin',
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        labels = {
            'Estado': '',
            'Ficha': '',
            'nombres_usuario': '',
            'apellidos_usuario': '',
            'idTipoDocumento': '',
            'numero_documento': '',
            'email_usuario': '',
            'numero_celular': '',
            'rol': '',
        }
        widgets = {
            'Estado': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'
            }),
            'Ficha': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'Ficha'
            }),
            'nombres_usuario': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'Nombres'
            }),
            'apellidos_usuario': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'Apellidos'
            }),
            'idTipoDocumento': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'
            }),
            'email_usuario': forms.EmailInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'placeholder': 'Email'
            }),
            'numero_documento': forms.NumberInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'min': 0,
                'placeholder': 'Número de Documento'
            }),
            'numero_celular': forms.NumberInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4',
                'min': 0,
                'placeholder': 'Número de Contacto'
            }),
            'rol': forms.Select(attrs={
                'placeholder': 'Rol',
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['idTipoDocumento'].empty_label = "Seleccione tipo de documento"
        self.fields['Estado'].empty_label = "Seleccione estado"
        self.fields['Ficha'].empty_label = "Seleccione una ficha"
        self.fields['rol'].empty_label = "Seleccione un rol"

class NuevoCandidatoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['rol']
        labels = {
            'rol': '',
        }
        widgets = {
            'rol': forms.Select(attrs={
                'placeholder': 'Rol',
                'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].empty_label = "Seleccione un rol"
        self.fields['rol'].initial = None
        
    

        
        