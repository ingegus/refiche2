# coding=UTF-8
from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
	url(r'^home/$', 'home'),
	url(r'^lesson/(?P<lesson_name>.+)$', 'lessonPage'),
	url(r'^upload/$', 'newSheetPage'),
	url(r'^download/(?P<pk>\d+)$', 'downloadSheetPage'),
	url(r'^classroom/$', 'classroomPage'),
	url(r'^media/(?P<ressource>.+)/(?P<url>.+)$', 'downloadRessource'),
)