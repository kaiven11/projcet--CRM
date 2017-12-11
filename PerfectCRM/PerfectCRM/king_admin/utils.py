#__author:  Administrator
#date:  2017/1/5


def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions = {}
    print('aaaa',request.GET.items())
    for k,v in request.GET.items():
        print(k,v)
        if v:
            filter_conditions[k] =v

    return admin_class.model.objects.filter(**filter_conditions),filter_conditions
