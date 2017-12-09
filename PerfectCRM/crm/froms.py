#coding=utf-8

from django.forms import ModelForm
from crm import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):

        for field_name, field_obj in cls.base_fields.items():

            # field_obj.widget.attrs['class'] = 'form-control'
            field_obj.widget.attrs['class'] = 'form-control'
            if field_name in EnrollmentForm.Meta.readonly_fields:
                field_obj.widget.attrs['disabled']='disabled'


        return ModelForm.__new__(cls)

    class Meta:
        model=models.Enrollment
        fields="__all__"
        exclude=['id','customer','contract_agreed','contract_approved']
        readonly_fields='customer'
    # def __new__(cls, *args, **kwargs):
    #     for field_name,field_obj in cls.base_fields.items():
    #         field_obj.wigst.attr='form_control'





#这里有一个问题 需要解决



#生成一个动态类，然后进行实例化


def create_dynamic_from(admins):
    def __new__(cls, *args, **kwargs):

        for field_name, field_obj in cls.base_fields.items():

            # field_obj.widget.attrs['class'] = 'form-control'
            field_obj.widget.attrs['class'] = 'form-control'
            if field_name in EnrollmentForm.Meta.readonly_fields:
                field_obj.widget.attrs['disabled'] = 'disabled'

        return ModelForm.__new__(cls)

    class Meta:
        model=admins
        fields='__all__'

    attr={'Meta':Meta}
    model_form=type('modelForm',(ModelForm,),attr)
    setattr(model_form,'__new__',__new__)

    return model_form






class CustomerFrom(ModelForm):

    class Meta:

        model=models.Customer
        fields = "__all__"
        exclude = ['qq_name', 'source', 'referral_from', 'consult_course', 'content', 'tags', 'memo']
        readonly_field=['qq','status','consultant']
        # error_messages ={
        #     'qq':{
        #         'required':_("QQ不能为空！"),
        #     },
        #
        #     'phone':{
        #         'required':_("手机号不能为空！"),
        #     }
        #
        #
        # }


    def __new__(cls, *args, **kwargs):

        for field_name, field_obj in cls.base_fields.items():

            # field_obj.widget.attrs['class'] = 'form-control'
            if field_name in cls.Meta.readonly_field:
                field_obj.widget.attrs['disabled']='disabled'
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)

    #进行form表单的验证

    def clean_qq(self):
        cleaned_qq=self.cleaned_data['qq'] #前端穿过来的
        db_qq=self.instance.qq
        if cleaned_qq!=db_qq:
            self.add_error('qq','请不要修改元数据！')
        return  cleaned_qq

    def clean_status(self):
        cleaned_status = self.cleaned_data['status']  # 前端穿过来的
        db_qq = self.instance.status
        if cleaned_status != db_qq:
            self.add_error('status', '请不要修改当前报名状态！')

        return cleaned_status

    def clean_consultant(self):
        cleaned_consultant = self.cleaned_data['consultant']  # 前端穿过来的
        db_qq = self.instance.consultant
        if cleaned_consultant != db_qq:
            self.add_error('consultant', '请不要修改当前咨询顾问！')

        return cleaned_consultant



class paymentForm(ModelForm):
    class Meta:
        model=models.Payment
        fields=['amount']