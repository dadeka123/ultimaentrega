from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import EquipoForm, JugadorForm, RepresentanteForm, UserEditForm, CustomUserCreationForm
from .models import *
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def inicio(request):
    try:
        avatar = Avatar.objects.get(user=request.user.id)
        url = avatar.image.url
    except Avatar.DoesNotExist:
        url = None
    return render(request, 'inicio.html', {'url': url})

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

class JugadorListView(LoginRequiredMixin, ListView):
    model = Jugador
    template_name = 'listaJugadores.html'
    login_url = '/App3/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipos = Equipo.objects.all()
        jugadores_por_equipo = {}
        for equipo in equipos:
            jugadores_por_equipo[equipo] = Jugador.objects.filter(equipo=equipo)
        context['jugadores_por_equipo'] = jugadores_por_equipo
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'Debe iniciar sesión para acceder a esta página')
        return super().dispatch(request, *args, **kwargs)

class RepresentanteListView(LoginRequiredMixin, ListView):
    model = Representante
    template_name = 'listaRepresentantes.html'
    login_url = '/App3/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        representantes = Representante.objects.all()
        jugadores_por_representante = {}
        for representante in representantes:
            jugadores_por_representante[representante] = Jugador.objects.filter(representante=representante)
        context['jugadores_por_representante'] = jugadores_por_representante
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'Debe iniciar sesión para acceder a esta página')
        return super().dispatch(request, *args, **kwargs)

from django.contrib.auth.mixins import LoginRequiredMixin

class EquipoListView(LoginRequiredMixin, ListView):
    model = Equipo
    template_name = 'listaEquipos.html'
    login_url = '/App3/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        equipos = Equipo.objects.all()
        jugadores_por_equipo = {}
        for equipo in equipos:
            jugadores_por_equipo[equipo] = Jugador.objects.filter(equipo=equipo)
        context['equipos'] = equipos
        context['jugadores_por_equipo'] = jugadores_por_equipo
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'Debe iniciar sesión para acceder a esta página')
        return super().dispatch(request, *args, **kwargs)


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

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url='/login/')
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



@login_required
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

@login_required
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

from django.contrib import messages
from django.views.decorators.cache import never_cache

@never_cache
def entrar(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request, data=request.POST)
        if formulario.is_valid():
            data = formulario.cleaned_data
            usuario = data['username']
            psw = data['password']
            user = authenticate(request, username=usuario, password=psw)
            if user is not None:
                login(request, user)
                messages.success(request, f'Ingreso exitoso')
                return redirect('inicio')
            else:
                messages.error(request, 'Error, datos incorrectos.')
    else:
        formulario = AuthenticationForm()
    return render(request, 'login.html', {'formulario': formulario})

def registrar(request):
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            username = formulario.cleaned_data.get('username')
            mensaje = f'Usuario {username} creado con éxito.'
            return redirect(reverse('inicio') + f'?mensaje={mensaje}')
    else:
        formulario = CustomUserCreationForm()
    return render(request, 'registro.html', {'formulario': formulario})
 
@never_cache    
@login_required     
def editar_perfil(request):
    usuario = request.user

    if request.method == 'POST':
        formulario = UserEditForm(request.POST, instance=request.user)

        if formulario.is_valid():
            data = formulario.cleaned_data
            usuario.email = data['email']
            usuario.first_name = data['first_name']
            usuario.last_name = data['last_name']
            usuario.set_password(data["password1"])
            usuario.save()

            messages.success(request, 'Datos actualizados.')
            return redirect('inicio')
        else:
            if formulario.errors.get('password2') and 'passwords do not match' in formulario.errors['password2']:
                formulario.add_error('password2', 'Las contraseñas no coinciden.')
            return render(request, 'editarPerfil.html', {'formulario': formulario, 'usuario': usuario})
    else:
        formulario = UserEditForm(instance=request.user)
        return render(request, 'editarPerfil.html', {'formulario': formulario, 'usuario': usuario})
