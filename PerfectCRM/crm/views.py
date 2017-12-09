from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from crm import models
from django.db import IntegrityError
from crm.backend.random_str import random_str
import os
from PerfectCRM import settings

from django.core.cache import cache

# Create your views here.

from crm import froms

def indexaa(request):

    return render(request,"index.html")

def customer_list(request):
    return render(request,"sales/customers.html")


#生成报名链接，提示将报名链接发送给学生

def enrollment_tackle(request,costomer_id):
    customer_obj = models.Customer.objects.get(id=costomer_id)
    msg={}
    if request.method=="GET":
        enroll_from_obj = froms.EnrollmentForm()
        return render(request,'sales/enroll.html',{'form_obj':enroll_from_obj,'customer_obj':customer_obj})

    elif request.method=="POST":
        enroll_from_obj = froms.EnrollmentForm(request.POST)
        if enroll_from_obj.is_valid():
            try: #在该表中有联合唯一的限制unique_together = ("customer","enrolled_class")，所以要抓去错误
                enroll_from_obj.cleaned_data['customer']=customer_obj
                #这里是因为models中含有三个字段为必须要填写的，而在Enrollform中并没有customer这个字段和前端对应，后端并不会接受该字段，所以需要在cleaned_data中添加相应的数据
                enroll_success_ret=models.Enrollment.objects.create(**enroll_from_obj.cleaned_data)
                if enroll_success_ret:  #给客户发送已经生成的报名表的链接，所以用报名表的id，而不是用户的ID
                    cache.set('random_str',random_str(),60000)
                    cache.set('enroll_id',enroll_success_ret.id,60000)
                    msg['link_url']='请将此报名链接发送给客户,http://127.0.0.1:8001/crm/enrollment/%s/registration/%s' % (cache.get('enroll_id'),cache.get('random_str'))


            except IntegrityError as e:


                enroll_obj=models.Enrollment.objects.get(customer=customer_obj,enrolled_class=enroll_from_obj.cleaned_data['enrolled_class'])
                enroll_id=enroll_obj.id

                if enroll_obj.contract_agreed:
                    return redirect('/crm/payment/%s' % enroll_id )

                cache.set('random_str', random_str(),60000)
                cache.set('enroll_id', enroll_id, 60000)

                msg['error']="该用户已经报名了此课程，请勿重复创建！"
                # 给客户发送已经生成的报名表的链接，所以用报名表的id，而不是用户的ID
                link_url='请将此报名链接发送给客户,http://127.0.0.1:8001/crm/enrollment/%s/registration/%s'% (cache.get('enroll_id'),cache.get('random_str'))

                msg['link_url'] =link_url

    return render(request, 'sales/enroll.html', {'form_obj': enroll_from_obj, 'customer_obj': customer_obj,"msg":msg})



#报名表的处理

def registration_tackle(request,enroll_id,random_str):

    enroll_obj=get_object_or_404(models.Enrollment,id=enroll_id)

    #判断是否是dropzone的ajax提交的数据

    if request.is_ajax(): # 判断提交的是否是ajax，然后对应的enroll_obj 建立相关的文件夹
        print('request.files',request.FILES)
        enroll_dir_id=os.path.join(settings.UPLOAD_URL,enroll_id)
        if not os.path.exists(enroll_dir_id):
            os.makedirs(enroll_dir_id,exist_ok=True)
        #If the target directory with the same mode as specified already exists, raises an OSError exception if exist_ok is False, otherwise no exception is raised.

        for k,file_obj in request.FILES.items():
            with open(os.path.join(enroll_dir_id,file_obj.name),'wb') as wr:
                for chunk in file_obj.chunks():
                    wr.write(chunk)




        return HttpResponse('aa')
    status =0

    if enroll_id:
            customer_obj=enroll_obj.customer
            if True :#cache.get('enroll_id'):
                if request.method=="POST":
                    customer_form=froms.CustomerFrom(request.POST,instance=customer_obj)
                    print(request.POST)
                    if customer_form.is_valid():
                        customer_form.save()
                        enroll_obj.contract_agreed=True
                        enroll_obj.save()
                        status=1
                        print("here")
                        return  render(request,'sales/registration.html',{'status':status})
                else:
                    print("here1111")
                    if enroll_obj.contract_agreed:
                        status=1

                    customer_form = froms.CustomerFrom(instance=customer_obj)


                return render(request,'sales/registration.html',{'customer_obj':customer_form,'enroll_obj':enroll_obj,'status':status})
            else:
                return HttpResponse('该链接已经失效')
    else:
        return HttpResponse("该链接不存在")



def payment_check(request,enroll_id):
    '''
    审核报名信息，不通过就驳回，否则就前进，显示客户信息，报名表的信息
    :param request:
    :param enroll_id:
    :return:
    '''

    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    customer_obj=enroll_obj.customer


    customer_form=froms.CustomerFrom(instance=customer_obj)
    # print(customer_form.Meta.flag,'............')
    # enroll_obj_form=froms.EnrollmentForm(instance=enroll_obj)
    #单纯一个obj类的对象不能进行循环吗？？，必须要用djangoform后才能循环

    print(customer_obj,type(customer_obj))
    return render(request,'sales/payment_check.html',{'customer_obj':customer_form,'enroll_obj':enroll_obj})



#信息审核不通过，驳回


def payment_notok(request,enroll_id):
    '''
    将学生报名表中的同意去掉，让学生重新填写相关信息，跳到相关页面
    :param request:
    :return:
    '''

    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_agreed=False
    enroll_obj.save()
    return redirect('/crm/enrollment/%s' % enroll_obj.customer.id)



def payment_ok(request,enroll_id):
    '''
    审核通过，转到付费界面
    :param request:
    :return:
    '''
    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    enroll_obj.contract_approved=True
    enroll_obj.save()

    return redirect('/crm/jiaofei/%s' % enroll_obj.id)


def jiaofei(request,enroll_id):
    '''
    缴费页面
    :param request:
    :return:
    '''

    #判断是否都已经同意了相关的协议和销售是否审核同意了

    errors={}

    enroll_obj = models.Enrollment.objects.get(id=enroll_id)
    customer_obj = enroll_obj.customer
    payment_obj = froms.paymentForm()
    customer_form = froms.CustomerFrom(instance=customer_obj)
    if request.method=="GET":

        if not enroll_obj.contract_approved and enroll_obj.contract_agreed:
            return redirect('/crm/enrollment/%s' % enroll_obj.customer.id)
        elif not enroll_obj.contract_approved:
            return render(request, 'sales/payment_check.html',
                          {'customer_obj': customer_form, 'enroll_obj': enroll_obj})
    # elif request.method=="POST":



    elif request.method=="POST":
        payment_obj = froms.paymentForm(instance=enroll_obj.customer)
        amount=int(request.POST.get('amount',0))
        if amount<500:
           errors['error']="数额不能低于500元！"
        else:

            a=models.Payment.objects.create(
                customer=customer_obj,
                course=enroll_obj.enrolled_class.course,
                amount=amount,
                consultant=enroll_obj.consultant,


            )

            enroll_obj.customer.status=0
            enroll_obj.customer.save()

            return  redirect('/myking_admin/crm/customer/')



    return render (request,'sales/jiaofei.html',{'customer_obj':customer_obj,'payment_obj':payment_obj,'enroll_obj':enroll_obj,'error':errors})