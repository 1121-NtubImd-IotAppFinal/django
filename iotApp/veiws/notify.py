import base64
from django.shortcuts import render
from ..models import notify, student
from iotApp.middleware import login_required
from ..module.linebotTemplate import *
from ..module.encrypt import *

'''
使用者訂閱網址：
https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=CN82GQa4zPRv2vaKU8BSr0&redirect_uri=https://birc.leedong.work/notify&scope=notify&state=NO_STATE
'''

@login_required
def notify_view(request):
    return render(request, 'web/linenotify/index.html')


def userBind(request):
    authorizeCode = request.GET['code']
    line_uid = decrypt_string(request.GET['state'])
    token = notify.getNotifyToken(authorizeCode)
    response_data = {'message': "綁定失敗 !"} 

    if(student.studentIsRegister(line_uid)):
        student_id = student.getStudentByLineUid(line_uid).student_id
        token2 = notify.getTokenByStudent(student_id)
        print(token)
        if(token2 != None):
            response_data = {'message': "您已完成通知設定，如有異常，請先移除原有綁定之後再次進行綁定 !"}
        if (notify.saveUserToken(token, student_id)):
            notify.lineNotifyMessage(token, "\n已經完成通知設定")
            response_data = {'message': "綁定成功 !"}
    else:
        response_data = {'message': "您尚未在LINE上設定個人資料"}


    return render(request, 'bind.html', context=response_data)

@login_required
def pushMessage(request):
    response_data = None
    if request.method=="POST":
        msg = "\n"+request.POST.get('msg')
        response_data = {'message': notify.pustAllUser(msg)}
    if response_data != None:
        return render(request, 'web/linenotify/index.html', response_data)
    else:
        return render(request, 'web/linenotify/index.html')

