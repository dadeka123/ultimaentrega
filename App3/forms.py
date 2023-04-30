from django import forms
from .models import Equipo, Jugador, Representante
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre_equipo', 'region', 'fecha_fundacion']
        widgets = {'fecha_fundacion': forms.DateInput(attrs={'type': 'date'})}

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = ['nombre', 'apellido', 'edad', 'equipo', 'posicion', 'titular']
        
class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['nombre', 'sitio_web', 'jugadores_contratados']
        
class UserEditForm(UserChangeForm):
    
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repetir contraseña", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['email'].label = 'Correo electrónico'
        self.fields['password'].label = ''
    
    def clean_password2(self):
        password2 = self.cleaned_data["password2"]
        if password2 != self.cleaned_data["password1"]:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2  
    
    def clean(self):
        cleaned_data = super(UserEditForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 or password2:
            if not password1 or not password2:
                raise forms.ValidationError("Debes ingresar ambas contraseñas.")
            elif password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Repetir contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeho lder': 'Repetir contraseña'}),
        strip=False,
    )

    error_messages = {
        'password_mismatch': "Las dos contraseñas no coinciden.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize error messages for password fields
        self.fields['password1'].error_messages = {
            'required': 'Por favor ingrese su contraseña.',
            'password_too_short': 'La contraseña debe contener al menos 8 caracteres.',
            'password_common': 'La contraseña es demasiado común.',
            'password_entirely_numeric': 'La contraseña no puede ser completamente numérica.',
        }

        self.fields['password2'].error_messages = {
            'required': 'Por favor confirme su contraseña.',
        }
        
        # Set empty string as error message for username field
        self.fields['username'].error_messages = {
            'required': '',
        }

