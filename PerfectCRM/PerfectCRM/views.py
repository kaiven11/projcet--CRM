from django.shortcuts import render,redirect

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


def acc_login(request):

    if request.method=="GET":
        print('here')
        return render(request,'login.html')


    elif request.method=="POST":
        print('here--post')
        _email=request.POST.get('email')
        _password=request.POST.get('password')
        user=authenticate(request,username=_email,password=_password)#用这个去验证，如果为真，返回一个数字
        print(user)
        if  user:
            login(request,user) #写入session
            return  redirect('/')
        else:
            return redirect('/account/login')


def acc_logout(request):
    logout(request)
    return redirect('/account/login')


def index(request):
    return render(request,"index.html")