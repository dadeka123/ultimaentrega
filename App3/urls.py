from django.contrib import admin
from django.urls import path
from PreEntrega3.views import *
from .views import *
from django.contrib.auth.views import LogoutView

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
    path('listaJugadores/', JugadorListView.as_view(), name="ListaJugadores"),
    path('listaRepresentantes/', RepresentanteListView.as_view(), name="ListaRepresentantes"),
    path('listaEquipos/', EquipoListView.as_view(), name="ListaEquipos"),
    path('eliminaJugador/<id>', eliminarJugador, name="EliminarJugador"),
    path('eliminaRepresentante/<id>', eliminarRepresentante, name="EliminarRepresentante"),
    path('eliminaEquipo/<id>', eliminarEquipo, name="EliminarEquipo"),
    path('editarJugador/<id>/', editar_jugador, name='EditarJugador'),
    path('editarEquipo/<id>/', editar_equipo, name='EditarEquipo'),
    path('editarRepresentante/<id>/', editar_representante, name='EditarRepresentante'),
    path('login/', entrar, name='Login'),
    path('registrar/', registrar, name='Registro'),
    path('salir/', LogoutView.as_view(template_name='salir.html'), name='Salir'),
    path('editar-perfil/', editar_perfil, name='EditarPerfil'),
]

