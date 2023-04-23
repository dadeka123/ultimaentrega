from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import EquipoForm, JugadorForm, RepresentanteForm
from .models import *

def agregar_equipo(request):
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaEquipos/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = EquipoForm()
    return render(request, 'agregar_equipo.html', {'form': form})

def agregar_jugador(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaJugadores/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = JugadorForm()
    return render(request, 'agregar_jugador.html', {'form': form})

def agregar_representante(request):
    if request.method == 'POST':
        form = RepresentanteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaRepresentantes/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = RepresentanteForm()
    return render(request, 'agregar_representante.html', {'form': form})

def busquedaEquipo(request):
    return render(request, "busquedaEquipo.html")

def buscarEquipo(request):
    if request.GET.get("Equipo"):
        equipo_name = request.GET.get("Equipo")
        equipos = Equipo.objects.filter(nombre_equipo=equipo_name)
        if equipos:
            return render(request, "resultadoBusqueda.html", {"equipos": equipos, "equipo_name": equipo_name})
        else:
            error_message = f"No se encontró ningún equipo con el nombre '{equipo_name}'."
            return render(request, "resultadoBusqueda.html", {"error_message": error_message})
    else:
        messages.error(request, "No enviaste información en el formulario.")
    return redirect('busquedaEquipo')

def busquedaJugador(request):
    return render(request, "busquedaJugador.html")

from django.db.models import Q

def buscarJugador(request):
    if request.GET.get("nombre_jugador") and request.GET.get("apellido_jugador"):
        nombre_jugador = request.GET.get("nombre_jugador")
        apellido_jugador = request.GET.get("apellido_jugador")
        jugadores = Jugador.objects.filter(Q(nombre=nombre_jugador) & Q(apellido=apellido_jugador))
        if jugadores:
            return render(request, "resultadoBusqueda2.html", {"jugadores": jugadores})
        else:
            mensaje_error = "No se encontró un jugador con ese nombre y apellido."
            return render(request, "resultadoBusqueda2.html", {"mensaje_error": mensaje_error})
    else:
        return render(request, "busquedaJugador.html")

def busquedaRepresentante(request):
    return render(request, "busquedaRepresentante.html")

def buscarRepresentante(request):
    if request.GET.get("nombre_representante"):
        nombre_representante = request.GET.get("nombre_representante")
        representantes = Representante.objects.filter(nombre=nombre_representante)
        if representantes:
            return render(request, "resultadoBusqueda3.html", {"representantes": representantes})
        else:
            mensaje_error = "No se encontró un representante con ese nombre."
            return render(request, "resultadoBusqueda3.html", {"mensaje_error": mensaje_error})
    else:
        form = RepresentanteForm()
        return render(request, "busquedaRepresentante.html", {'form': form, 'errors': form.errors})

def listaJugadores(request):
    
    equipos = Equipo.objects.all()
    jugadores_por_equipo = {}
    for equipo in equipos:
        jugadores_por_equipo[equipo] = Jugador.objects.filter(equipo=equipo)
    return render(request, 'listaJugadores.html', {'jugadores_por_equipo': jugadores_por_equipo})

def listaRepresentantes(request):
    
    representantes = Representante.objects.all()
    jugadores_por_representante = {}
    for representante in representantes:
        jugadores_por_representante[representante] = Jugador.objects.filter(representante=representante)
    return render(request, 'listaRepresentantes.html', {'jugadores_por_representante': jugadores_por_representante})

def listaEquipos(request):
    equipos = Equipo.objects.all()
    jugadores_por_equipo = {}
    for equipo in equipos:
        jugadores_por_equipo[equipo] = Jugador.objects.filter(equipo=equipo)
    return render(request, 'listaEquipos.html', {'equipos': equipos, 'jugadores_por_equipo': jugadores_por_equipo})

def eliminarJugador(request, id):
    
    if request.method == 'POST':
        
        jugador = Jugador.objects.get(id=id)
        jugador.delete()
        return redirect('/App3/listaJugadores/')

def eliminarEquipo(request, id):
    
    if request.method == 'POST':
        
        equipo = Equipo.objects.get(id=id)
        equipo.delete()
        return redirect('/App3/listaEquipos/')
    
def eliminarRepresentante(request, id):
    
    if request.method == 'POST':
        
        representante = Representante.objects.get(id=id)
        representante.delete()
        return redirect('/App3/listaRepresentantes/')

def editar_jugador(request, id):
    jugador = Jugador.objects.get(id=id)
    
    if request.method == 'POST':
        form = JugadorForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaJugadores/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = JugadorForm(instance=jugador)        
    return render(request, 'editar_jugador.html', {'form': form, 'id': id})

def editar_equipo(request, id):
    equipo = Equipo.objects.get(id=id)
    
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaEquipos/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = EquipoForm(instance=equipo)        
    return render(request, 'editar_equipo.html', {'form': form, 'id': id})

def editar_representante(request, id):
    representante = Representante.objects.get(id=id)
    
    if request.method == 'POST':
        form = RepresentanteForm(request.POST, instance=representante)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/App3/listaRepresentantes/')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = RepresentanteForm(instance=representante)        
    return render(request, 'editar_representante.html', {'form': form, 'id': id})
