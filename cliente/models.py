import email
from django.db import models

# Create your models here.
class Cliente(models.Model):    
    GLN_Cliente = models.CharField(primary_key=True, max_length=250)

    def __str__(self):
        return self.GLN_Cliente

    class Meta:
        ordering = ['GLN_Cliente']
        db_table = 'cliente'
        managed = True