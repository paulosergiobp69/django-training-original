from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AutenticacaoConfig(AppConfig):
    name = 'autenticacao'
    verbose_name = _('autenticacao')

    def ready(self):
        import autenticacao.signals  # noqa
        
