# Generated by Django 2.2.7 on 2019-12-17 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lancamento', '0004_auto_20191206_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='lancamento',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='lancamento_user_fk', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lancamento',
            name='tipolancamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tipolancamento_fk', to='lancamento.TipoLancamento'),
        ),
    ]
