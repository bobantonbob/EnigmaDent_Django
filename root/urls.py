from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Enigma Dent — Адміністрування'
admin.site.site_title = 'Enigma Dent Admin'
admin.site.index_title = 'Керування заявками, відгуками та контентом'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('departments/', include('departments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
