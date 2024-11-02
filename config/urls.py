from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Adicione 'accounts/' para todas as rotas
    path('locations/', include('locations.urls')),
    path('inventory/', include('inventory.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('methodology/', include('methodology.urls')),
    path('', RedirectView.as_view(url='/accounts/login/')),  # Redireciona para a página de login
    #path('analysis/', include('analysis.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
