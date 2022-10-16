from django.db import models
import datetime
from sucursal.models import Sucursal

fecha = datetime.datetime.today()

class Inventario(models.Model):
    id_i = models.AutoField(primary_key=True)    
    FechaInventario = models.DateField(default=fecha)
    GLN_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return self.GLN_sucursal

    class Meta:
        ordering = ['id_i']