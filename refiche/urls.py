from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^', include('accueil.urls')),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'accueil/login_accueil.html'}),
    url(r'^app/', include('app.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^register/', include('registration.urls')),
    url(r'^facebook/', include('facebook.urls')),
]
