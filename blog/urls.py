from django.conf.urls import url
from blog import views

app_name = 'blog'

urlpatterns = [
	url(r'^$', views.home, name='home'),
]