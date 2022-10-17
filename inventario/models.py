from pyexpat import model
from django.db import models
from sucursal.models import Sucursal

class Inventario(models.Model):
    id_i = models.AutoField(primary_key=True)    
    FechaInventario = models.CharField(max_length=250)
    Inventario_Final = models.IntegerField()
    GLN_sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    def __str__(self):
        return self.GLN_sucursal

    class Meta:
        ordering = ['id_i']
        db_table = 'inventario'
        managed = True