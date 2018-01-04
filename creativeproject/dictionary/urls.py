from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name = 'dictionary'
urlpatterns = [
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^search/(?P<translation>(enar|aren))/(?P<dialect>(Gulf|Levantine|Egyptian))/(?P<word>([\u0600-\u06FF]*|[A-Za-z0-9_]*))/$', views.search_page, name='search'),
    url(r'^getjson/(?P<translation>(enar|aren))/(?P<dialect>(Gulf|Levantine|Egyptian))/(?P<word>([\u0600-\u06FF]*|[A-Za-z0-9_]*))/$', views.json_search, name='jsonsearch'),
    url(r'^create/$', views.create_entry_page, name='create'),
    url(r'^submit/$', views.submit_entry, name='submit'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^submit_comment/$', views.submit_comment, name='submit_comment'),
    url(r'^entries/(?P<translation>(enar|aren))/(?P<dialect>(Gulf|Levantine|Egyptian))/(?P<word>([\u0600-\u06FF]*|[A-Za-z0-9_]*))/$', views.entries, name='search'),
]
