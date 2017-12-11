from django.shortcuts import render,HttpResponse
from crm import models
import os
from PerfectCRM import settings
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
    elif request.is_ajax():
        file_path = os.path.join(settings.UPLOAD_HOME_WORK_URL, stu_obj.student.customer.name,
                                 stu_obj.course_record.from_class.course.name, str(stu_obj.course_record.day_num))
        print(file_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        for k, v in request.FILES.items():
            print(dir(v))
            with open(os.path.join(file_path,v.name), 'wb') as fw:
                for chunks in v.chunks():
                    fw.write(chunks)
        return HttpResponse({"status": "ok"})
    elif request.method=="POST":
        print(request.FILES)

        #下面是创建目录的形式

    #    /student_name/course_name/study_the_xx

        # file_path=settings.UPLOAD_HOME_WORK_URL.join(stu_obj.student.customer.name,stu_obj.course_record.from_class,stu_obj.course_record.day_num)






    return render(request,'student/homework_detail.html',{'i':stu_obj})