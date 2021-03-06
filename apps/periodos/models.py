from django.db import models
from apps.estado_seguimiento.models import Glo_EstadoSeguimiento
# Create your models here.

# Create your models here.
class Glo_EstadoPeriodo(models.Model):
    estado= models.IntegerField()
    descripcion_periodo= models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.descripcion_periodo)


class Glo_Periodos(models.Model):
    descripcion_periodo = models.CharField(max_length=100)
    anio_periodo= models.IntegerField()
    fecha_inicio=models.DateField(blank=True, null=True)
    fecha_termino=models.DateField(blank=True, null=True)
    id_estado = models.ForeignKey(Glo_EstadoPeriodo, on_delete=models.PROTECT, null=True)


    def __str__(self):
        return '{}'.format(self.descripcion_periodo)



class Glo_Seguimiento(models.Model):
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True, blank=True)
    fecha_inicio= models.DateTimeField(blank=True, null=True)
    fecha_termino= models.DateTimeField(blank=True, null=True)
    descripcion_seguimiento = models.CharField(max_length=100, null=True, blank=True)
    fecha_inicio_corte=models.DateField(blank=True, null=True)
    fecha_termino_corte=models.DateField(blank=True, null=True)

    id_estado_seguimiento= models.ForeignKey(Glo_EstadoSeguimiento, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.descripcion_seguimiento)

class Glo_validacion(models.Model):
    id_periodo= models.ForeignKey(Glo_Periodos, on_delete=models.PROTECT, null=True, blank=True)
    id_periodo_seguimiento = models.ForeignKey(Glo_Seguimiento, on_delete=models.PROTECT, null=True, blank=True)
    fecha_inicio= models.DateTimeField(blank=True, null=True)
    fecha_termino= models.DateTimeField(blank=True, null=True)
    id_estado_periodo= models.ForeignKey(Glo_EstadoSeguimiento, on_delete=models.PROTECT, null=True, blank=True)
    descripcion_validacion = models.CharField(max_length=100, null=True, blank=True)
