
from django.conf.urls import url
from crm import views

urlpatterns = [
    url(r'^$', views.indexaa,name="sales_index"),
    url(r'^customers/$', views.customer_list,name="customer_list"),
    url(r'^enrollment/(\d+)$', views.enrollment_tackle,name="enrollment_tackle"),
    url(r'^payment/(\d+)$', views.payment_check,name="payment_check"),
    url(r'^notok/(\d+)$', views.payment_notok,name="payment_not"),
    url(r'^ok/(\d+)$', views.payment_ok,name="payment_ok"),
    url(r'^jiaofei/(\d+)$', views.jiaofei,name="jiaofei"),
    url(r'^enrollment/(\d+)/registration/(\w+)$', views.registration_tackle,name="registration_tackle"),
]
