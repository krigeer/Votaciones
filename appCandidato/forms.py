from django import forms
from votos.models import Candidato, Propuesta, Postulacion, Cualidad

class Actualizar_foto(forms.ModelForm):
    class Meta:
        model = Candidato
        fields = ['foto', 'vacante', 'cualidades']
        widgets = {
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'vacante': forms.Select(attrs={'class': 'form-control'}),
            'cualidades': forms.CheckboxSelectMultiple(),
        }


class ActualizarPropuesta(forms.ModelForm):
    class Meta:
        model = Propuesta
        fields = ['titulo', 'descripcion', 'video']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'}),
            'descripcion': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'}),
            'video': forms.ClearableFileInput(attrs={'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500 mb-4'}),
        }


