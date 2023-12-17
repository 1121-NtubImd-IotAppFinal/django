from django.utils import timezone
from django.db.models import Sum 
from django.core.paginator import Paginator
from django.shortcuts import render
from ..models import student
from iotApp.models import sign
from ..module.workdays import *
from iotApp.middleware import login_required

@login_required
def manager(request):
    current_datetime = timezone.now().date()
    students = student.objects.all()
    paginator = Paginator(students, 15)
    page_number = request.GET.get('page', 1)
    students_on_page = paginator.get_page(page_number)

    for student_instance in students_on_page:
        student_instance.create_time = student_instance.create_time.date()
        X = get_workdays(student_instance.create_time, current_datetime) * 3
        Y = sign.objects.filter(student=student_instance).aggregate(total_hours=Sum('hours'))['total_hours']
        missing_hours = X - Y if Y is not None else X
        student_instance.X = X
        student_instance.Y = Y if Y is not None else 0
        student_instance.missing_hours = missing_hours

    # 对 students_on_page 根据 missing_hours 从大到小排序
    students_on_page = sorted(students_on_page, key=lambda student: student.missing_hours, reverse=True)

    return render(request, 'leader/manager.html', {'students': students_on_page})
