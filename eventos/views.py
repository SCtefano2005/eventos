from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from usuarios.models import Usuario
from empresa.models import Empleado
from .models import *
from .forms import *
from django.contrib import messages
from django.utils import timezone
import pandas as pd

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            empleado = Empleado.objects.get(email=email)
            if check_password(password, empleado.password):
                # Establecer la sesión
                request.session['empleado_id'] = empleado.id
                request.session['empleado_nombre'] = empleado.nombre
                return redirect('dashboard')
            else:
                error = 'Credenciales incorrectas'
        except Empleado.DoesNotExist:
            error = 'El empleado no existe'
        return render(request, 'login.html', {'error': error})
    
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  
    return redirect('logint')

def login_required(func):
    def wrapper(request, *args, **kwargs):
        if 'empleado_id' not in request.session:
            return redirect('logint')
        return func(request, *args, **kwargs)
    return wrapper

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/crear_usuario.html', {'form': form})

@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


@login_required
def listar_eventos(request):
    eventos = Evento.objects.prefetch_related('asistentes').all()  
    return render(request, 'eventos/listar_eventos.html', {'eventos': eventos})

@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'eventos/crear_evento.html', {'form': form})

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)  
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento) 
        if form.is_valid():
            form.save()  
            return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)  
    return render(request, 'eventos/editar_evento.html', {'form': form})

@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('listar_eventos')
    return render(request, 'eventos/eliminar_evento.html', {'evento': evento})


@login_required
def inscribir_usuario(request):
    usuarios = Usuario.objects.all()
    eventos = Evento.objects.all()

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('listar_eventos')
            except ValidationError as e:
                print(f"Error: {e}")
                return render(request, 'inscripcion/inscribir_usuario.html', {
                    'form': form, 
                    'error': e.message,
                    'usuarios': usuarios,
                    'eventos': eventos
                })
        else:
            print(form.errors)
    else:
        form = InscripcionForm()
    return render(request, 'inscripcion/inscribir_usuario.html', {
        'form': form,
        'usuarios': usuarios,
        'eventos': eventos
    })
    
@login_required
def desinscribir_usuario(request, evento_id, usuario_id):
    if request.method == "POST":
        evento = get_object_or_404(Evento, id=evento_id)
        usuario = get_object_or_404(Usuario, id=usuario_id)  
        if request.session.get('empleado_id'):  
            try:
                inscripcion = Inscripcion.objects.get(evento=evento, usuario=usuario)
                inscripcion.delete()
                messages.success(request, 'El usuario se ha desinscrito del evento exitosamente.')
            except Inscripcion.DoesNotExist:
                messages.error(request, 'El usuario no está inscrito en este evento.')
        else:
            messages.error(request, 'No tienes permiso para realizar esta acción.')

    return redirect('listar_usuarios')  
 
@login_required    
def exportar_usuarios(request):
    usuarios = Usuario.objects.all().values()  
    df_usuarios = pd.DataFrame(usuarios)
    eventos = Evento.objects.all().values() 
    df_eventos = pd.DataFrame(eventos)
    inscripciones = Inscripcion.objects.all().values()  
    df_inscripciones = pd.DataFrame(inscripciones)
    fecha_descarga = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    fecha_formateada = timezone.now().strftime('%Y-%m-%d')
    response['Content-Disposition'] = f'attachment; filename=usuarios_{fecha_formateada}.xlsx'
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df_usuarios.to_excel(writer, index=False, sheet_name='Usuarios')
        worksheet = writer.sheets['Usuarios']
        worksheet.cell(row=1, column=7, value='Fecha de descarga')
        worksheet.cell(row=1, column=8, value=fecha_descarga)
        if not df_eventos.empty:
            df_eventos['fecha'] = pd.to_datetime(df_eventos['fecha']).dt.tz_localize(None) 
        df_eventos.to_excel(writer, index=False, sheet_name='Eventos')
        if not df_inscripciones.empty:
            df_inscripciones['fecha'] = pd.to_datetime(df_inscripciones['fecha']).dt.tz_localize(None)  
        df_inscripciones.to_excel(writer, index=False, sheet_name='Inscripciones')
    return response

@login_required    
def buscar_eventos_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    eventos_inscritos = Inscripcion.objects.filter(usuario=usuario)
    eventos_creados = Evento.objects.filter(creador=usuario)
    context = {
        'usuario': usuario,
        'eventos_inscritos': eventos_inscritos,
        'eventos_creados': eventos_creados
    }

    return render(request, 'inscripcion/buscar_eventos_usuario.html', context)
