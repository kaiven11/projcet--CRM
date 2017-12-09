#coding=utf-8

from django import template
from django.db.models import DateField,DateTimeField
from django.utils.safestring import mark_safe
from django.utils import timezone
from newkindadmin.myadmin import enroll
from django.db.models import Sum
from crm import models
register = template.Library()

@register.simple_tag
def conut_study (i,user_obj):

    study_count=models.CourseRecord.objects.filter(from_class=i.enrolled_class).count()
    return study_count


@register.simple_tag
def sum_grade(obj):

    course_record=models.CourseRecord.objects.filter(from_class=obj.enrolled_class)
    # print(course_record)
    grade=models.StudyRecord.objects.filter(student=obj,course_record__in=course_record).aggregate(Sum('score'))
    print(grade)

    return grade