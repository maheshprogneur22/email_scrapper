from django.contrib import admin
from django.urls import path

from . import views
from .views import home




from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),

    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
