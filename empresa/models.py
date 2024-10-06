from django.db import models
from django.contrib.auth.hashers import make_password

class Empleado(models.Model):
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=250)
    email = models.EmailField(max_length=300, unique=True)
    password = models.CharField(max_length=500)
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Empleado, self).save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
