from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from eventos.models import Evento, Inscripcion

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.password):
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                return redirect('home')
            else:
                error = 'Credenciales incorrectas'
        except Usuario.DoesNotExist:
            error = 'El usuario no existe'
        return render(request, 'logint.html', {'error': error})
    
    return render(request, 'logint.html')

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')
        return func(request, *args, **kwargs)
    return wrapper

@login_required
def home(request):
    usuario_nombre = request.session.get('usuario_nombre', 'Invitado')
    eventos = Evento.objects.all() 
    return render(request, 'home.html', {'usuario_nombre': usuario_nombre, 'eventos': eventos})

@login_required
def create_evento(request):
    if request.method == 'POST':
        nombre_evento = request.POST['nombre']
        descripcion = request.POST['descripcion']
        fecha_evento = request.POST['fecha']
        Evento.objects.create(
            nombre=nombre_evento,
            descripcion=descripcion,
            fecha=fecha_evento,
            creador_id=request.session.get('usuario_id')
        )
        return redirect('ver_eventos')

    return render(request, 'eventos/create_evento.html')

@login_required
def ver_eventos(request):
    usuario_id = request.session.get('usuario_id')
    eventos = Evento.objects.exclude(creador_id=usuario_id)
    inscripciones = Inscripcion.objects.filter(usuario_id=usuario_id).values_list('evento_id', flat=True)
    eventos = eventos.exclude(id__in=inscripciones)
    return render(request, 'eventos/ver_eventos.html', {'eventos': eventos})

@login_required
def mis_eventos(request):
    usuario_id = request.session.get('usuario_id')
    eventos_creados = Evento.objects.filter(creador_id=usuario_id)
    inscripciones = Inscripcion.objects.filter(usuario_id=usuario_id).values_list('evento_id', flat=True)
    eventos_inscritos = Evento.objects.filter(id__in=inscripciones)
    for evento in eventos_creados:
        evento.numero_participantes = Inscripcion.objects.filter(evento=evento).count()
    for evento in eventos_inscritos:
        evento.numero_participantes = Inscripcion.objects.filter(evento=evento).count()
    return render(request, 'eventos/mis_eventos.html', {
        'eventos_creados': eventos_creados,
        'eventos_inscritos': eventos_inscritos  
    })

@login_required
def modificar_evento(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        if evento.creador_id != request.session.get('usuario_id'):
            messages.error(request, 'No tienes permiso para modificar este evento.')
            return redirect('ver_eventos')
    except Evento.DoesNotExist:
        messages.error(request, 'El evento no existe.')
        return redirect('ver_eventos')

    if request.method == 'POST':
        evento.nombre = request.POST['nombre']
        evento.descripcion = request.POST['descripcion']
        evento.fecha = request.POST['fecha']
        evento.save()
        messages.success(request, 'Evento modificado exitosamente.')
        return redirect('ver_eventos')

    return render(request, 'eventos/modificar_evento.html', {'evento': evento})

@login_required
def inscribirme_evento(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        Inscripcion.objects.create(usuario_id=request.session.get('usuario_id'), evento=evento)
        messages.success(request, 'Te has inscrito al evento exitosamente.')
    except Evento.DoesNotExist:
        messages.error(request, 'El evento no existe.')

    return redirect('ver_eventos')

@login_required
def eliminar_evento(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        if evento.creador_id == request.session.get('usuario_id'):
            evento.delete()
            messages.success(request, 'Evento eliminado exitosamente.')
        else:
            messages.error(request, 'No tienes permiso para eliminar este evento.')
    except Evento.DoesNotExist:
        messages.error(request, 'El evento no existe.')

    return redirect('ver_eventos')

@login_required
def desinscribirme_evento(request, evento_id):
    try:
        inscripcion = Inscripcion.objects.get(usuario_id=request.session.get('usuario_id'), evento_id=evento_id)
        inscripcion.delete()
        messages.success(request, 'Te has desinscrito del evento exitosamente.')
    except Inscripcion.DoesNotExist:
        messages.error(request, 'No estás inscrito en este evento.')

    return redirect('ver_eventos')

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')  

