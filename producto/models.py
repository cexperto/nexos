from email.policy import default
from operator import imod
from django.db import models
from cliente.models import Cliente

import datetime

fecha = datetime.datetime.today()

class Producto(models.Model):
    id_p = models.AutoField(primary_key=True)
    Gtin_Producto= models.CharField(max_length=250)
    PrecioUnidad = models.CharField(max_length=250)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)    

    def __str__(self):
            return self.Gtin_Producto