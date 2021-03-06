from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from os.path import join

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('accueil.urls', namespace='accueil')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'accueil/login_accueil.html'}),
    url(r'^app/', include('app.urls', namespace='app')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^register/', include('registration.urls', namespace='registration')),
    url(r'^facebook/', include('facebook.urls', namespace='facebook')),
] + static(settings.MEDIA_URL + 'sheet-thumbnails/', document_root=join(settings.MEDIA_ROOT, 'sheet-thumbnails')) \
	+ static(settings.MEDIA_URL + 'webpage-thumbnails/', document_root=join(settings.MEDIA_ROOT, 'webpage-thumbnails')) \
	+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)