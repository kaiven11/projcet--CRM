#__author:  Administrator
#date:  2017/1/5

from crm import models


enabled_admins = {}

class BaseAdmin(object):
    list_display = []
    list_filters = []
    list_per_page = 20

class CustomerAdmin(BaseAdmin):
    list_display = ['qq','name','source','consultant','consult_course','date','status']
    list_filters = ['source','consultant','consult_course','status']
    #model = models.Customer

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer','consultant','date')


def register(model_class,admin_class=None):
    if model_class._meta.app_label not in enabled_admins:
        enabled_admins[model_class._meta.app_label] = {} #enabled_admins['crm'] = {}
    #admin_obj = admin_class()
    admin_class.model = model_class #绑定model 对象和admin 类
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class
    #enabled_admins['crm']['customerfollowup'] = CustomerFollowUpAdmin


register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)



