#coding=utf-8

from django import template
from django.db.models import DateField,DateTimeField
from django.utils.safestring import mark_safe
from django.utils import timezone
from newkindadmin.myadmin import enroll
register = template.Library()



@register.simple_tag
def display_verbose_name(admins):
    return admins.model._meta.verbose_name



#显示列
@register.simple_tag
def dis_data(data,column,admins):
    ret_str=""
    try:
        file_obj=data._meta.get_field(column)
        if file_obj.choices: #  如果是choice类型，就只能get_xxx_display() 方法来显示具体的内容
                ele=getattr(data,"get_%s_display"%column)()

        else:
               ele=getattr(data,column)
        if type(ele).__name__=='datetime':  #判断是否是日期类型，如果是就做相应的处理
            ele=ele.strftime("%Y-%m-%d %H:%M:%S")

        # if type(file_obj).__name__=='AutoField':
        if column=='id': #判断是否是ID，如果是就默认按此排序

            ret_str='''<td><a href="%s">%s</a></td>'''%(str(getattr(data,'id'))+'/change',getattr(data,column))
        else:
            ret_str= '<td>%s</td>'%ele
    except:

        url_link='/crm/enrollment/%s' % data.id

        ret_=enroll(admins).format(baoming_url=url_link)

        ret_str='<td>%s</td>'%ret_

    return mark_safe(ret_str)


#检索功能的编写

@register.simple_tag

def dis_filter_data(admins,filters,filter_condition):
    file_obj=admins.model._meta.get_field(filters)
    select_biaoti="<select class ='form-control' name={aa} ><option value ='' > ------ </option >"
    str1='</select>'
    if file_obj.choices:
        for choice_item in file_obj.choices:
            selected=""
            # print(type(choice_item[0]),type(filter_condition.get(filters))
            if filter_condition.get(filters)==str(choice_item[0]): #判断当前检索条件是否已经选中过
                selected="selected"
                select_biaoti+="<option value=%s %s>%s</option>"%(choice_item[0],selected,choice_item[1])



                selected=''
            else:
                select_biaoti+= "<option value=%s %s>%s</option>" % (choice_item[0], selected, choice_item[1])

        select_biaoti += str1

    if type(file_obj).__name__=="ForeignKey":
            selected = ""
            for choice_item in file_obj.get_choices()[1:]:
                if filter_condition.get(filters) == str(choice_item[0]): #判断当前检索条件是否已经选中过
                    selected = "selected"
                    select_biaoti += "<option value=%s %s>%s</option>" % (choice_item[0], selected, choice_item[1])

                    selected=''

                else:
                    select_biaoti += "<option value=%s %s>%s</option>" % (choice_item[0], selected, choice_item[1])

            select_biaoti += str1
    date_list=['DateField','DateTimeField']
    #如果是日期类型的，我们做的条件是
    '''
    近一天
    近三天
    近一周
    近三个月
    近半年
    近一年
    '''
    if type(file_obj).__name__ in date_list:

        #近一天
        date_filter=[]
        current_date=timezone.now().date()
        oneday=current_date-timezone.timedelta(days=1)
        thereday=current_date-timezone.timedelta(days=3)
        sevenday=current_date-timezone.timedelta(days=7)
        theremothons=current_date-timezone.timedelta(days=90)
        halfyear=current_date-timezone.timedelta(days=180)
        oneyear=current_date.replace(month=1,day=1)
        date_list=[]
        date_list.append(['今天',current_date])
        date_list.append(['近一天',oneday])
        date_list.append(['近三天',thereday])
        date_list.append(['近一周',sevenday])
        date_list.append(['近三个月',theremothons])
        date_list.append(['近半年',halfyear])
        date_list.append(['近一年',oneyear])

        selected=''
        for  d in date_list:
            print((filter_condition.get('date__gte')),str(d[1]))
            if filter_condition.get('date__gte')==str(d[1]):
                selected="selected"


            else:
                selected = ''
            select_biaoti += "<option value=%s %s>%s</option>" % (d[1], selected, d[0])


        select_biaoti += str1
        select_biaoti=select_biaoti.format(aa=filters+'__gte')

    else:
        select_biaoti=select_biaoti.format(aa=filters)


    return mark_safe(select_biaoti)



'''
source=&consultant=1&consult_course=&status=
'''


#排序功能的链接的实现
@register.simple_tag
def build_list(filter_condition, item,oo,admins):
    ele='<th>'
    tiaojian=''

#传入reqeust.GET.copy()对象，包含了修改后的数据
    print(oo.__dict__)
    for k,v in filter_condition.items():
        if v:
            tiaojian+='%s=%s&'%(k,v)




    if oo.get('o'):

        if item.strip('-')==oo.get('o').strip('-'):#排序功能的实现
            tiaojian+='o=%s'% oo.get('o')
        else:
            if not hasattr(admins.model,item):  #判断新增字段不在数据库里的方式
                print(hasattr(admins.model._meta.get_field,item))
            else:

                tiaojian += 'o=%s' % item
    else:
        tiaojian+='o=%s' %admins.ordering if admins.ordering else item

    if oo.get('s'):
        tiaojian+='&s=%s' %(oo.get('s'))






    ele+='''<a class='test' href=?%s>%s</a></th>'''%(tiaojian,item)
    # ele.format(url=tiaojian,item=item)


    return mark_safe(ele)


#分页上一页的实现
@register.simple_tag
def build_page(filter_condition,posts):

    tiaojian=''
    for k,v in filter_condition.GET.items():
        if k=='p':
            continue
        if v:
            tiaojian += '&%s=%s' % (k, v)
    ele = '<a href = "?p=%s%s" > 上一页 </a>' % (posts.previous_page_number(),tiaojian)

    return mark_safe(ele)



 # <a href="?p={{ posts.next_page_number }}">Next</a>

# 分页下一页的实现
@register.simple_tag
def build_page_next(filter_condition,posts):
    tiaojian = ''
    for k, v in filter_condition.GET.items():
        if k == 'p':
            continue
        if v:
            tiaojian += '&%s=%s' % (k, v)
    ele = '<a href = "?p=%s%s" > 下一页 </a>' % (posts.next_page_number(), tiaojian)

    return mark_safe(ele)

# #改变seacherfiled的提交地址
# @register.simple_tag
# def build_form(request):
#     url_name= '''<form class="form-inline" action={d}>'''
#     tiaojian=''
#     for k,v in request.items():
#         if k=='s':
#             continue
#         tiaojian+='%s=%s&'%(k,v)
#
#     url_name=url_name.format(d=tiaojian)
#
#     return mark_safe(url_name)


#搜索框的实现


ss='''
<input type="text" name="s" class="form-control" value='{value_text}' id="exampleInputAmount" placeholder="{hoder}">
'''

@register.simple_tag
def dis_search_text(request):
    if request.GET.get('s'):
        oo=ss.format(value_text=request.GET.get('s'),hoder='')

    else:
        oo=ss.format(hoder='输入用户名或者密码',value_text='')
    return mark_safe(oo)


#for test some fields attr and method

@register.simple_tag
def man (filed):
    print(dir(filed))
    print(filed)

@register.simple_tag
def fields_item_list(fields,admins,sp_obj):
        '''
        m2m 的数据，这个实在admin中配置的 horizontal

        :param fields:
        :param admins:
        :param sp_obj:
        :return:
        '''
        tags_list=getattr(admins.model,fields).rel.to.objects.all()

        return enumerate(tags_list)


@register.simple_tag
def selected_list(sp_obj,fields_name):
    '''
    返回所有已经选择的m2m的数据

    :param sp_obj:
    :param fields_name:
    :return:
    '''
    print('---------------------------',sp_obj.instance)
    if sp_obj.instance.id:
        aa=getattr(sp_obj.instance,fields_name).all()
        return enumerate(aa)