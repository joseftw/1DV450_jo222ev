from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'labb.views.home', name='home'),
    # url(r'^labb/', include('labb.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # First - url to match, second = path to view
    
    url(r'^login/$', 'labb1.views.login_user', name="login"),
    url(r'^logout/$', 'labb1.views.logout_user', name="logout"),
    url(r'^home/$', 'labb1.views.home', name="home"),

    url(r'^projects/$', 'labb1.views.project_list', name="project_list"),
    url(r'^projects/(?P<project_id>\d+)/$', 'labb1.views.project_show', name="project_show"),
    url(r'^projects/(?P<project_id>\d+)/join/$', 'labb1.views.project_join', name="project_join"),
    url(r'^projects/(?P<project_id>\d+)/delete/$', 'labb1.views.project_delete', name="project_delete"),
    url(r'^projects/(?P<project_id>\d+)/edit/$', 'labb1.views.project_edit', name="project_edit"),
    url(r'^projects/add/$', 'labb1.views.project_add', name="project_add"),
    url(r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)/$', 'labb1.views.ticket_show', name="show_one_ticket"),
    url(r'^projects/(?P<project_id>\d+)/tickets/$', 'labb1.views.project_show_tickets', name="project_show_tickets"),
    url(r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)/delete/$', 'labb1.views.project_delete_ticket', name="project_delete_ticket"),
    url(r'^projects/(?P<project_id>\d+)/tickets/(?P<ticket_id>\d+)/edit/$', 'labb1.views.ticket_edit', name="ticket_edit"),
    url(r'^projects/(?P<project_id>\d+)/tickets/add/$', 'labb1.views.project_add_ticket', name="project_add_ticket"),
    url(r'^admin/', include(admin.site.urls)),
)
