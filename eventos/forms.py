from django import forms 
from usuarios.models import Usuario
from .models import *


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'creador']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Cambiado a DateTimeInput
        }
        
class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['evento', 'usuario']