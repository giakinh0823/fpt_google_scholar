from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



app_name='home'

urlpatterns = [
    path('', views.home, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import handler404, handler500, handler403, handler400

handler404 = views.handler404
handler500 = views.handler500