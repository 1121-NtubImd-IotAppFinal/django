from django.utils import timezone
from django.db.models import Sum 
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from ..models import student
from iotApp.models import sign,setting
from ..module.workdays import *
from iotApp.middleware import login_required

@login_required
def manager(request):
    current_datetime = timezone.now().date()
    students = student.objects.all()
    paginator = Paginator(students, 15)
    page_number = request.GET.get('page', 1)
    students_on_page = paginator.get_page(page_number)
    default_hour_norm = 3

    setting_instance = setting.objects.first()

    for student_instance in students_on_page:
        student_instance.create_time = student_instance.create_time.date()
        X = get_workdays(student_instance.create_time, current_datetime) * (float(setting_instance.hour_norm) if setting_instance and setting_instance.hour_norm != 0 else default_hour_norm)
        Y = sign.objects.filter(student=student_instance).aggregate(total_hours=Sum('hours'))['total_hours']
        missing_hours = 0
        if(Y!=None and X!=None):
            missing_hours = f'{(X - Y):.2f}' if (Y<X) else 0
        student_instance.X = f'{X:.2f}'
        student_instance.Y = f'{Y:.2f}'if Y is not None else 0
        student_instance.missing_hours = missing_hours

    students_on_page = sorted(students_on_page, key=lambda student: student.missing_hours, reverse=True)

    return render(request, 'leader/manager.html', {'students': students_on_page})