#coding=utf-8
from crm import models
from django.shortcuts import redirect,HttpResponse
from django.forms import ModelForm,ValidationError
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.conf import settings


class BaseAdmin(object):
    list_display=[]
    list_filters=[]
    list_perpage =4
    search_field=[]
    ordering=None
    filter_horizontal=[] #显示多对多的样式
    readonly_fields=[]
    readonly_table = False
    actions=['delete_objs']

    def delete_objs(self, request, queryset):
        print('delete_objec------------')

    delete_objs.short_description = "delete the selected objects"


#学生记录表
class StudentRecordAdmin(BaseAdmin):
    list_display = ['student','course_record','attendance','score','date']
    list_filters=['score','date','course_record']


#老师上课记录表

class CourseRecordAdmin(BaseAdmin):
    list_display = ['from_class', 'day_num', 'teacher', 'has_homework', 'homework_title','outline','date']
    actions = ['initialize_studentrecord', 'delete_objs']


    '''
    #初始化学生上课记录表
    '''
    def initialize_studentrecord(self, request, queryset):
        course_record_obj=models.CourseRecord.objects.get(id=queryset[0])
        student_all=course_record_obj.from_class.enrollment_set.all()
        queryset_list=[]
        for student_cls in student_all:
            student_obj=models.StudyRecord(student=student_cls,
                                           course_record=course_record_obj,
                                           )
            queryset_list.append(student_obj)
        models.StudyRecord.objects.bulk_create(queryset_list)

        return redirect('/myking_admin/crm/studyrecord/?course_record=%s'%queryset[0])

class CustomerAdmin(BaseAdmin):
    list_display = ['id','qq','name','phone','source','consultant','consult_course','date','status','enroll',]
    list_filters = ['source','consultant','consult_course','status','date']
    list_perpage=10
    search_field = ['qq','name','consultant__name']
    ordering = '-id'
    filter_horizontal=['tags',]
    readonly_fields=['qq','consultant',]
    readonly_table=False




    #model = models.Customer

class CustomerFollowUpAdmin(BaseAdmin):

    list_display = ['id','customer','consultant','date']
    list_filters = ['customer', 'consultant']
    list_perpage=4


class UserProfileAdmin(BaseAdmin):
    list_display = ['id','email','name']
    search_field = [ 'name']
    readonly_fields=['password']
    readonly_table=True





def enroll(self):
    # print(self.instance)
    return '<a href="{baoming_url}">报名</a>'


#返回到前台的数据结构

# {'crm':{tb1:admin,
#   tb2:admin1,
# }}


#生成一中数据结构

query_set_dic={}

def register(models,admins):
    if models._meta.app_label not in query_set_dic:
        query_set_dic[models._meta.app_label]={}


    admins.model=models
    query_set_dic[models._meta.app_label][models._meta.model_name]=admins

    return query_set_dic


a=register(models.Customer, CustomerAdmin)
a=register(models.CustomerFollowUp, CustomerFollowUpAdmin)
a=register(models.UserProfile,UserProfileAdmin)
a=register(models.StudyRecord,StudentRecordAdmin)
a=register(models.CourseRecord,CourseRecordAdmin)
#每一个类对应一个modelform，我们要用动态类进行动态的生成。



def MymodelForm(admins,request=None):

    '''
    __init__是当实例对象创建完成后被调用的，然后设置对象属性的一些初始值。
    __new__是在实例创建之前被调用的，因为它的任务就是创建实例然后返回该实例，是个静态方法。
    也就是，__new__在__init__之前被调用，__new__的返回值（实例）将传递给__init__方法的第一个参数，然后__init__给这个实例设置一些参数。
    :param admins: 
    :return: 
    
    '''

    #动态添加到form中去进行验证  这个是对所有的表单数据进行验证  这个是用于修改操作，添加操作是不会运行的

    def form_clean(self):


        print('self.instance.id',self.instance.id)
        clean_data=self.cleaned_data
        print('test------',self.cleaned_data)
        error_list=[]
        if  self.instance.id:
            print('实例化对象',self.instance,'daozheli')

            for item in admins.readonly_fields:
                houtai_submit= getattr(self.instance,item) #后台的数据，从数据库传过来的  instance

                fron_web_submit=self.cleaned_data.get(item,None)

                if fron_web_submit != houtai_submit:
                    error_list.append(  ValidationError(('Invalid value: %(value)s'),params={"value": '元数据不正确'},))

        self.ValidationError = ValidationError
        if error_list:
            raise ValidationError(error_list)




    #对单个数据进行验证

    def clean_name(self):

        # memo_length=getattr(self.instance,'memo')# from db
        print('memo is running------------')

        print('test2................',self.cleaned_data)
        name_from_web=self.cleaned_data.get('name') # from web
        if not name_from_web:
            self.add_error('name', "姓名不能为空！")

        return name_from_web  # 自定义 clean 和 clean_filed 在验证完以后一定要返回验证后的数据



    def __new__(cls, *args, **kwargs):

        for field_name,field_obj in cls.base_fields.items():
            print('字段',field_name)
            #判断是否字段在 只读字段中
            # field_obj.widget.attrs['class'] = 'form-control'
            if not admins.add_form: #如果不是在添加表单中，就不要添加disabled 属性了
                if field_name in admins.readonly_fields:
                    field_obj.widget.attrs['disabled']='disabled'

        return ModelForm.__new__(cls)




    class Meta:
        model=admins.model
        fields="__all__"
        exclude={'last_login'}

    attr={'Meta':Meta}
    _model_class_form=type('Mymodel',(ModelForm,),attr)
    # setattr(_model_class_form, 'clean_memo', clean_memo)
    setattr(_model_class_form,'__new__',__new__)
    setattr(_model_class_form,'clean',form_clean)
    setattr(_model_class_form,'clean_name',clean_name)

    print(_model_class_form)
    return _model_class_form











