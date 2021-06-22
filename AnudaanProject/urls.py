from django.conf.urls import i18n,static
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from Accounts.views import generate_otp,otp
def switch_lang_code(path, language):
 
    # Get the supported language codes
    lang_codes = [c for (c, name) in settings.LANGUAGES]
 
    # Validate the inputs
    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)
 
    # Split the parts of the path
    parts = path.split('/')
 
    # Add or substitute the new language prefix
    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language
 
    # Return the full new path
    return '/'.join(parts)

def index(request):
    return redirect('admin/')

urlpatterns = i18n.i18n_patterns(
    path('admin/login/',generate_otp, name='admin:login'),
    path('admin/login/otp/',otp, name='otp'),
    path('admin/', admin.site.urls),
    
    path('chaining/', include('smart_selects.urls')),
    prefix_default_language=False
)+static.static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

admin.site.site_header=_('Anudan Project')
admin.site.site_url =''
admin.site.index_title=_('Home')
admin.site.site_title=_('Anudan Project')
