from django.db import models

# Create your models here.
class RegistroMovimento(models.Model):

    id_objeto = models.PositiveIntegerField()
    processo = models.CharField(max_length=50)
    valor = models.FloatField(null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)