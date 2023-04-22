from django.contrib import admin
from django.urls import path
from PreEntrega3.views import *
from .views import *

urlpatterns = [
    path('', inicio, name="inicio"),
    path('agregar-equipo/', agregar_equipo, name="agregar_equipo"),
    path('agregar-jugador/', agregar_jugador, name="agregar_jugador"),
    path('agregar-representante/', agregar_representante, name="agregar_representante"),
    path('busquedaEquipo/', busquedaEquipo, name="busquedaEquipo"), 
    path('buscarEquipo/', buscarEquipo, name="BuscarEquipo"),
    path('busquedaJugador/', busquedaJugador, name="BusquedaJugador"),
    path('buscarJugador/', buscarJugador, name="BuscarJugador"),
    path('busquedaRepresentante/', busquedaRepresentante, name='busquedaRepresentante'),
    path('buscarRepresentante/', buscarRepresentante, name="BuscarRepresentante"),
    path('listaJugadores/', listaJugadores, name="ListaJugadores"),
    path('listaRepresentantes/', listaRepresentantes, name="ListaRepresentantes"),
]

