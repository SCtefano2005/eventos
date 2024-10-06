from django.db import models
from django.core.exceptions import ValidationError
from usuarios.models import Usuario

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    
class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='asistentes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.usuario == self.evento.creador:
            raise ValidationError('No puedes unirte a tu propio evento')
        
    
    
    def save(self, *args, **kwargs):
        self.clean()
        super(Inscripcion, self).save(*args, **kwargs)