from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from iotApp.middleware import login_required
from ..models import student

@login_required
def delete_student(request, student_id):
    if request.method == 'POST':
        student_instance = get_object_or_404(student, id=student_id)
        student_instance.delete()
        return redirect('people')
    else:
        return HttpResponseForbidden("Forbidden")

@login_required
def people(request):
    if request.method == 'POST':
        # 如果是 POST 請求，表示用戶點擊了刪除按鈕
        # 在這裡執行刪除操作，這裡以一個簡單的例子做演示
        student_ids_to_delete = request.POST.getlist('delete_student')
        student.objects.filter(student_id__in=student_ids_to_delete).delete()
        return redirect('people')  # 跳轉到某個頁面或重新導向

    # 如果是 GET 請求，渲染網頁
    students = student.objects.all()
    return render(request, 'leader/people.html', {'students': students})
