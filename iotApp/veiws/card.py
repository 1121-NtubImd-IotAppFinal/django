from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from iotApp.middleware import login_required
from ..models import student, card

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def delete_card(request, card_id):
    try:
        if request.method == 'POST':
            card_instance = get_object_or_404(card, card_id=card_id)
            card_instance.delete()
            if card_instance.student:
                return redirect('cardman', student_id=card_instance.student.student_id)
            else:
                return redirect('cardman')
    except:
        return redirect('cardman')

    return HttpResponse("Method Not Allowed", status=405)
# 修改 cardman 视图
@login_required
def cardman(request):
    all_students = student.objects.all()

    selected_student = request.GET.get('filter_student', '')
    
    if selected_student:
        filtered_cards = card.objects.filter(student__student_id=selected_student)
    else:
        filtered_cards = card.objects.all()

    # 指定每頁顯示的卡片數量
    cards_per_page = 15
    paginator = Paginator(filtered_cards, cards_per_page)

    page = request.GET.get('page')
    try:
        filtered_cards = paginator.page(page)
    except PageNotAnInteger:
        filtered_cards = paginator.page(1)
    except EmptyPage:
        filtered_cards = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        card_ids_to_delete = request.POST.getlist('delete_card')
        if card_ids_to_delete:
            card.objects.filter(card_id__in=card_ids_to_delete).delete()
            return redirect('cardman')

    # 檢查是否有資料
    if not filtered_cards:
        message = "查無符合篩選條件的資料。"
    else:
        message = None

    return render(request, 'leader/cardman.html', {'filtered_cards': filtered_cards, 'all_students': all_students, 'selected_student': selected_student, 'message': message})
