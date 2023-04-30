from django.http import HttpResponse
from django.template import Template, Context, loader
from App3.views import *
from App3.templates import *

def lista_equipos(request):
    
    plantilla = loader.get_template("equipos.html")
    equipos = plantilla.render({
        "equipos": [
            {"nombre": "Real Madrid"},
            {"nombre": "Barcelona"},
            {"nombre": "Peñarol"},
            {"nombre": "Sacachispa"},
        ]
    })
     
    return HttpResponse(equipos)

# aca se hace blabla = f'esta es la lista de jugadores: {lista_jugadores}'
#return httpresponse (blabla)

def lista_jugadores(request):
           
    plantilla = loader.get_template("jugadores.html")
    documento = plantilla.render({
        "jugadores": [
            {"nombre": "Arezo", "titular": True},
            {"nombre": "Darwin", "titular": True},
            {"nombre": "Ronaldo", "titular": False},
            {"nombre": "Messi", "titular": False},
        ]
    })
     
    return HttpResponse(documento)

def representantes(self):
    
     plantilla = loader.get_template("representantes.html")
     lista_managers = plantilla.render({
        "managers": [
            {"nombre": "Ramon"},
            {"nombre": "Jacinto"},
            {"nombre": "Pedro"},
            {"nombre": "Jousepe"},
        ]
    })
     
     return HttpResponse(lista_managers)

def agregar_jugador(self, nombre, equipo):
    
    agregar_jugador = Jugador(nombre=nombre, equipo=equipo)
    agregar_jugador.save()
    
    return HttpResponse(f"""
    <p>El jugador {Jugador.nombre} se agregó al equipo {Jugador.equipo}</p>
    """)
    
def inicio(self):
    
    return render(self, "inicio.html")


@login_required
def my_view(request):
    messages.error(request, "This is an error message.", extra_tags='danger')
