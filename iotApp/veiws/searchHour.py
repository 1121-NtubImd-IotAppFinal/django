from datetime import datetime, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from iotApp.middleware import login_required
from ..models import sign, student, image
from django.http import JsonResponse

@login_required
def frontend(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    student_id = request.GET.get('std')
    page = request.GET.get('page')
    all_students = student.get_all_students()

    if not start_date:
        start_date_time = date(1900, 1, 1)
    else:
        start_date_time = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date_time = date.today()
    else:
        end_date_time = datetime.strptime(end_date, '%Y-%m-%d')

    records = sign.objects.filter(date__gte=start_date_time, date__lte=end_date_time).order_by('-sign_id')

    if student_id and student_id != "all":
        records = records.filter(student__student_id=student_id)

    images = image.objects.filter(sign__in=records)

    paginator = Paginator(records, 15)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    return render(request, 'leader/searchHour.html', {'records': records, 'students': all_students, 'start_date': start_date, 'end_date': end_date, 'images': images})