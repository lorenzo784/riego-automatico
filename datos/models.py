from django.db import models
from django.utils import timezone

class RegistroRiego(models.Model):
    cantidad_agua = models.FloatField()
    fecha_hora = models.DateTimeField(default=timezone.now)
