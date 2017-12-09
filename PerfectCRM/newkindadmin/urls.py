
from django.conf.urls import url
from django.contrib import admin
from newkindadmin import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^(\w+)/(\w+)/$',views.dis_obj,name='dis_obj'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.update_data,name='update_obj'),
    url(r'^(\w+)/(\w+)/(\d+)/change/password/$',views.change_password,name='change_password'),
    url(r'^(\w+)/(\w+)/add/$',views.add_data,name='add_obj'),

]
