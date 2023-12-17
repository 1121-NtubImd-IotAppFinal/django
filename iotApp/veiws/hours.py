from django.shortcuts import render
from django.db.models import Sum
from iotApp.middleware import login_required
from ..models import sign

@login_required
def hours(request):
    late_attendance_records = sign.objects.values('student__student_id') \
        .annotate(total_hours=Sum('hours'))

    return render(request, 'leader/hours.html', {'late_attendance_records': late_attendance_records})
