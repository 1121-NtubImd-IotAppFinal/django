from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from iotApp.middleware import login_required
from ..models import sign, student

@login_required
def later(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    student_id = request.GET.get('std')
    page = request.GET.get('page')
    late_attendance_records = sign.objects.filter(isLate=True).order_by('-sign_id')
    all_students = student.get_all_students()

    if start_date:
        start_date_time = datetime.strptime(start_date, '%Y-%m-%d')
        late_attendance_records = late_attendance_records.filter(date__gte=start_date_time)
    if end_date:
        end_date_time = datetime.strptime(end_date, '%Y-%m-%d')
        late_attendance_records = late_attendance_records.filter(date__lte=end_date_time)
    if student_id and student_id != "all":
        late_attendance_records = late_attendance_records.filter(student_id=student_id)

    paginator = Paginator(late_attendance_records, 15)  
    try:
        late_attendance_records = paginator.page(page)
    except PageNotAnInteger:
        late_attendance_records = paginator.page(1)
    except EmptyPage:
        late_attendance_records = paginator.page(paginator.num_pages)

    return render(request, 'leader/later.html', {'late_attendance_records': late_attendance_records, 'students': all_students, 'start_date': start_date, 'end_date': end_date})
