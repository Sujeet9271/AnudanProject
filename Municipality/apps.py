from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MunicipalityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Municipality'
    verbose_name = _('Municipality')
