import email
from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_c = models.AutoField(primary_key=True)
    GLN_Cliente = models.CharField(max_length=250)
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.GLN_Cliente

    class Meta:
        ordering = ['id_c']