from django import forms

class LoginForm(forms.Form):
    documento = forms.IntegerField(
        label='Número de Documento',
        widget=forms.NumberInput(attrs={'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500', 'placeholder': 'Ingresa tu número de documento'}),
    )

    contrasena = forms.CharField(
        label='Contraseña',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'shadow appearance-none border rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-green-500', 'placeholder': 'Ingresa tu contraseña'}),
        )
    # remember_me = forms.BooleanField(required=False, label='Recordarme')



