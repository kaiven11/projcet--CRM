from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from newkindadmin import myadmin

from django.contrib.auth.decorators import login_required

from crm.backend.error_list import  *

# Create your views here.
from newkindadmin.myadmin import *
@login_required
def index(request):

    return render(request, 'myking_admin/myking_index.html', {
        'obj':a,
    })

@login_required
def dis_obj(request,app_name,table_name):
    #找到admins，得到model对象
    # print(app_name,table_name)
    admins=query_set_dic[app_name][table_name]

    if request.method=="POST":
        # print('it is post here')
        action=request.POST.get('action')
        select_ids=request.POST.get('select_id')
        if hasattr(admins,action):
            func=getattr(admins,action)
            return func(admins,request,select_ids)



    # 得到admin里预先设置的所要取得的数据
    filter_condition={}
    #去除关键字
    key_word=['p','o','s']
    for k,v in request.GET.items():
        if k in key_word:
            continue

        if v:
            filter_condition[k]=v


    o=request.GET.get('o')
    request_copy=request.GET.copy()
    print(request_copy)

    #排序功能的实现

    # source=0&consultant=&consult_course=&status=&date__gte=&s=

    #构造searchfiled



    all_list=admins.model.objects.filter(**filter_condition)
    search_field = request.GET.get('s', None)

    if search_field:
        con = Q()
        con.connector = 'OR'
        for i in admins.search_field:
            con.children.append((i, search_field))
        obj=all_list.filter(con)
    else:
        obj=all_list

    if request.GET.get('o'):

        obj=obj.order_by(request.GET.get('o')) #通过过虑器得到总的数据然后进行分页

        if o.startswith('-'):

            request_copy.update({'o':o.strip('-')})
        else:
           request_copy.update({'o':'-'+o})

    else:
        obj=obj.order_by(admins.ordering if admins.ordering else '-id')





    #分页的实现
    current_page = request.GET.get('p')

    paginator = Paginator(obj,admins.list_perpage) #确定分页的数据进行分页
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象
    try:
        posts = paginator.page(current_page) #取当前页进行对象
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表
        # number                当前页
        # paginator             paginator对象
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)





    print(obj)
    return render(request,'myking_admin/orm_obj.html',{'admins':admins,'objs':posts,'filter_condition':filter_condition,'posts':posts,
                                                       'o':request_copy

                                                       })




#更新数据

@login_required
def update_data(request,app_name,table_name,obj_id):


        admins = query_set_dic[app_name][table_name]

        # print(obj_id)
        instance_obj =admins.model.objects.get(id=obj_id)
        admins.add_form=False
        form_obj = myadmin.MymodelForm(admins,request)
        if request.method=="GET":

            form_obj=form_obj(instance=instance_obj)
            return render(request,'myking_admin/updateobj.html',{'sp_obj':form_obj,'admin_class':admins})
        elif request.method=="POST":
            if not admins.readonly_table:  #防止前端进行恶意添加提交按钮进行提交
                form_obj=form_obj(request.POST,instance=instance_obj)
                if form_obj.is_valid(): #会调用clean方法，clean方法会给到 cleaned_data数据列表中
                    form_obj.save()
                    # return render(request, 'myking_admin/updateobj.html', {'sp_obj': form_obj, 'admin_class': admins})
                    return redirect('/'.join(request.path.split('/')[:-3]))
                return render(request, 'myking_admin/updateobj.html', {'sp_obj': form_obj, 'admin_class': admins})

        return render(request, 'myking_admin/updateobj.html', {'sp_obj': form_obj(instance=instance_obj), 'admin_class': admins})


@login_required
def add_data(request,app_name,table_name):
    admins = query_set_dic[app_name][table_name]
    admins.add_form = True
    print(admins.filter_horizontal)
    form_obj=myadmin.MymodelForm(admins,request)

    if request.method=="GET":
        form_obj=form_obj()
        return render(request,'myking_admin/addobj.html',{'sp_obj':form_obj,'admin_class':admins})

    elif request.method=="POST":
        form_obj=form_obj(request.POST)

        if form_obj.is_valid(): #调用to_python() 和validate 两个方法，如果没有问题就放入到cleaned_data里面。
            print(form_obj)
            form_obj.save()
            return redirect('/'.join(request.path.split('/')[:-2]))

    return render(request, 'myking_admin/addobj.html', {'sp_obj': form_obj, 'admin_class': admins})


#修改密码

@login_required
def change_password(request,app_name,table_name,user_id):
    admins = query_set_dic[app_name][table_name]
    # print(obj_id)
    instance_obj = admins.model.objects.get(id=user_id)
    admins.add_form = False

    if request.method == "GET":



        return render(request, 'myking_admin/password_change.html', { 'obj': instance_obj})

        # 将传入的数据加入到字典中，可以返回
    elif request.method=="POST":
        old = request.POST.get('p1')
        new = request.POST.get('p2')
        if old==new:
            instance_obj.set_password(new)
            instance_obj.save()
            return  redirect(request.path.rstrip('password/'))
        else:
            print('herehrehrhehrherhere')
            a= BaseResponse()
            a.message={"invalid":"两次输入的密码不同"}
            return  render(request,'myking_admin/password_change.html',{"error":a,'obj':instance_obj})

