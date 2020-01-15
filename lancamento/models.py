from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TipoLancamento(models.Model):
    descricao = models.CharField(max_length=50)

    def __str__(self):
        return str(self.id) + ' - ' + self.descricao

class Lancamento(models.Model):

    descricao = models.CharField(max_length=100)
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    tipolancamento = models.ForeignKey(TipoLancamento, on_delete=models.PROTECT, related_name='tipolancamento_fk', null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='lancamento_user_fk', null=True)
    
    models.Index(fields=['data'], name='lancamento_idx01')

class LancamentoItem(models.Model):

    lancamento = models.ForeignKey(Lancamento, on_delete=models.PROTECT, related_name='itenslancamento')
    descricao = models.CharField(max_length=100)
    valor = models.FloatField()

class Receita(models.Model):

    descricao = models.CharField(max_length=100)
    valor = models.FloatField()
    data = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='receita_user_fk', null=True)
