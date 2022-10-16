from django.db import models
import datetime

from requests import delete
from producto.models import Producto

fecha = datetime.datetime.today()

class Sucursal(models.Model):
    id_s = models.AutoField(primary_key=True)
    GLN_Sucursal = models.CharField(max_length=250)    
    nombre = models.CharField(max_length=250)
    Gtin_Producto_fk = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.GLN_Sucursal
