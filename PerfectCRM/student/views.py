from django.shortcuts import render
from crm import models
# Create your views here.


def index(request):
    return render(request,"student/index.html")


def stu_detail(request,enroll_id,class_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    class_obj=models.ClassList.objects.get(id=class_id)
    course_obj=models.CourseRecord.objects.filter(from_class=class_obj)
    study_records=models.StudyRecord.objects.filter(student=enroll_obj,course_record__in=course_obj)
    print(study_records)
    return render(request,"student/course_detail.html",{'study_record':study_records,'enroll_ment':enroll_obj})


def homework_detail(request,study_record_id):
    stu_obj=models.StudyRecord.objects.get(id=study_record_id)
    if request.method=="GET":
        pass
    elif request.method=="POST":
        print(request.FILES)
    return render(request,'student/homework_detail.html',{'i':stu_obj})