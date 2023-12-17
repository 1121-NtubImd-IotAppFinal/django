from django.utils import timezone
from django.db.models import Sum 
from django.core.paginator import Paginator
from django.shortcuts import render
from ..models import setting, student
from iotApp.models import sign
from ..module.workdays import *
from iotApp.middleware import login_required

@login_required
def student_h(request, student_id):
    try:
        student_instance = student.objects.get(student_id=student_id)
        current_datetime = timezone.now().date()
        hourNorm = setting.objects.first().hour_norm
        student_instance.create_time = student_instance.create_time.date()
        print(hourNorm)
        X = get_workdays(student_instance.create_time, current_datetime) * hourNorm
        Y = sign.objects.filter(student=student_instance).aggregate(total_hours=Sum('hours'))['total_hours']
        missing_hours = X - Y if Y is not None else X
        student_instance.X = X
        student_instance.Y = Y if Y is not None else 0
        student_instance.missing_hours = missing_hours

        return render(request, 'leader/student_h.html', {'student': student_instance})
    except student.DoesNotExist:
        return render(request, 'leader/student_not_found.html')  # 处理学生未找到的情况

