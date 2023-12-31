# yourapp/views.py
import uuid
import os
import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from ..models import card, image, sign, notify
from iotAppFinalproject import settings
from ..module import encrypt, image_regonition

@csrf_exempt
def report(request):
    if request.method == 'POST':
        sign_id = request.POST.get('sign_id')
        reportText = request.POST.get('reportText')
        if sign_id != None and reportText != None:
            sign_instance = sign.objects.get(sign_id=encrypt.decrypt_string(sign_id))
            if(sign_instance != None):
                if(sign_instance.affair == ""):
                    sign_instance.affair = reportText
                    sign_instance.save()
                    return render(request, 'report.html', {'success': '回報成功 !','token': sign_id,'student':sign_instance.student.student_id + sign_instance.student.name
                                    ,"date":sign_instance.date,"in":sign_instance.check_in_time,"out":sign_instance.check_out_time
                                     ,"affair":sign_instance.affair})
                else:
                    return render(request, 'report.html', {'error': '回報失敗: 因為此編號已經完成回報 !'})
            else:
                return render(request, 'report.html', {'error': '編號錯誤 !'})
        else:
            return render(request, 'report.html', {'error': '資料未填寫完整'})
    elif request.method == 'GET':
        try:
            token = request.GET.get('token')
            sign_id = encrypt.decrypt_string(token)
            sign_instance = sign.objects.get(sign_id=sign_id)
            return render(request, 'report.html', {'token': token,'student':sign_instance.student.student_id + sign_instance.student.name
                                                   ,"date":sign_instance.date,"in":sign_instance.check_in_time,"out":sign_instance.check_out_time
                                                   ,"affair":sign_instance.affair})
        except: 
            return render(request, 'report.html', {'error': '發生錯誤'})
        
@csrf_exempt
def cardCheck(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        print(card_id)
        student = card.getStudentByCardId(card_id)
        if student == None:
            return HttpResponse(f'No', status=200, content_type='text/plain')
        else:
            return HttpResponse(f'Yes', status=200, content_type='text/plain')

@csrf_exempt
def image_check(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        toekn = request.POST.get('token')
        uploaded_file = request.FILES.get('file')
        if toekn == "p+8bwe~s_74;`?%nq}#?t7~p7_rr6qe_&###@*ky//}f^!_b=&00852!sr:sz!a":
            if(image_regonition.detect_face(uploaded_file)):
                return HttpResponse(checkin_Out(card_id, uploaded_file), status=200, content_type='text/plain; charset=utf-8')
    return HttpResponse(f'error', status=200, content_type='text/plain')

def checkin_Out(card_id, uploaded_file):
    student = card.getStudentByCardId(card_id)
    if student == None:
        return None
    else:
        req = sign.getOrCreateSign(student)
        sign_id = req[0]
        in_Out = req[1]
        time = req[2]
        hours = req[3]
        token = notify.getTokenByStudent(student.student_id)
        if token != None:
            notifyMsg = f"\n\n {student.name} 您好\n\n"
            if in_Out == "in":
                notifyMsg += f"您已在 {time} 時進行簽到 !\n"
                notifyMsg += f"當前已經開始計算時數中。"

            else:
                signToken = encrypt.encrypt_string(str(sign_id))
                notifyMsg += f"您已在 {time} 時進行簽退 !\n"
                notifyMsg += f"時數經計算為：{hours}小時。"
                notifyMsg += f"==================\n"
                notifyMsg += f"請至以下連結填寫今日進度\n"
                notifyMsg += f"https://birc.leedong.work/report?token={signToken}"
        
            notify.lineNotifyMessage(token, notifyMsg)
        saveImage(uploaded_file, sign_id)
        text = f'{sign_id},{in_Out},{student.student_id},{student.name}'
        return text
        
               

@csrf_exempt
def saveImage(uploaded_file,sign_id):
    if uploaded_file:                
        current_date = datetime.datetime.now()
        year = str(current_date.year)
        month = str(current_date.month).zfill(2)
        day = str(current_date.day).zfill(2)
        
        # 隨機檔名
        uuid_str = str(uuid.uuid4())
        file_extension = os.path.splitext(uploaded_file.name)[1]
        random_filename = f"{uuid_str}{file_extension}"

        # 存檔
        upload_path = os.path.join('images', year, month, day, random_filename)
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        filename = fs.save(upload_path, uploaded_file)

        file_path = fs.url(filename)
        new_student = image(path=file_path, sign_id=int(sign_id), create_time=current_date)
        new_student.save()
        print("File saved at:", file_path)