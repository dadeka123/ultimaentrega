from django import forms
from .models import Equipo, Jugador, Representante

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