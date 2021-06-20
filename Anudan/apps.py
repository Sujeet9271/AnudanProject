from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AnudanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Anudan'
    verbose_name = _('Grant')
