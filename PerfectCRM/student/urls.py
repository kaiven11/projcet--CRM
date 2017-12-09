
from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$', views.index,name="stu_index"),
    url(r'^detail/(\d+)/(\d+)$', views.stu_detail,name="stu_detail"),
    url(r'^home_work_detail/(\d+)$', views.homework_detail,name="homework_detail"),

]
