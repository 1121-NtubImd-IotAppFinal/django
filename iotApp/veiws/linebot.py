import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from ..module import mqtt
from ..module.linebotTemplate import *
from ..models import student,notify,card


line_bot_api = LineBotApi('R6/InwkZD1rg5brgHLv7bAjIvhpsDzBViLDwFZyPi7fpvQr2vTdqFBsQW0PS6twbAHLy450mr08rudWYTx6UDpE9DNW98O5XzL22LlNKjwxEy16k1BYrE9wqra6Ft4xRoHqcTx/uG97tljx8nuPK1gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7a5e182b0df20870823a444aa3a17913')
rich_menu_isRigister = "richmenu-bcb996e6bb583f0fd6b7cfb4e542e3f0"
rich_menu_NotRigister = "richmenu-f1c9a746b43cbee082fca356fad2dfad" 

@csrf_exempt
def line_bot_webhook(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@csrf_exempt
@handler.add(FollowEvent)
def handle_follow_event(event):
    user_id = event.source.user_id
    if(student.studentIsRegister(user_id)):
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_isRigister)
    else:
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_NotRigister)
        welcome_message = "歡迎使用本系統！\n請先輸入您的名字和學號以完成綁定。"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

@csrf_exempt
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    if(student.studentIsRegister(user_id)):
        student_instance = student.getStudentByLineUid(user_id) 
        student_id = student_instance.student_id
        notifyFind = notify.userIsFind(student_id) #是否綁定通知
        if(message_text == "@設定通知"):
            template_message = notify_send(user_id, notifyFind)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif(message_text == "@移除通知綁定"):
            if (notifyFind):
                notify.removeUser(student_id)
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="移除通知成功 !"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="您尚未進行通知綁定 !"))
        elif(message_text == "@設定卡片"):
                template_message = card_send()
                line_bot_api.reply_message(event.reply_token, template_message)
        elif(message_text == "@新增卡片"):
            mqtt.send_mqtt_message(student_id , "card/register")
            txt = "請在十秒內攜帶您的卡片前往簽到退設備\n"
            txt += "看到亮橘燈後請靠卡即可進行卡片綁定\n\n"
            txt += "注意: \n1.已經註冊的卡片不得重複綁定."
            txt += "\n2.最多只能綁定10張卡片."
            txt += "\n3.未亮橘燈請重新操作"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=txt))
        elif("@刪除卡片" in message_text):
            card_id = str(message_text).replace("@刪除卡片","")
            req = card.deleteStudentCard(card_id)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=req))
        elif(message_text == "@管理卡片" ):
            template_message = getCardListByStudent(student_id)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif(message_text == "@查詢欠缺時數"):
            req = getLackHour(student_instance)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=req))
        elif(message_text == "@查詢簽到退紀錄"):
            template_message = getSignListByStudent(student_id)
            line_bot_api.reply_message(event.reply_token, template_message)
        elif(message_text == "完成註冊"):
            line_bot_api.link_rich_menu_to_user(user_id, rich_menu_isRigister)

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="尚未輸入個人資料"))


@csrf_exempt
def register(request):
    response_data = {"message": "註冊成功"}
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            stdId = data.get('std_id')
            LineUid = data.get('line_uid')
            studentAcc = student.objects.filter(student_id=stdId).first()
            lineAcc = student.objects.filter(line_uid=LineUid).first()
            if studentAcc !=  None:
                response_data = {"message": "該學號已被註冊"}
            elif lineAcc != None:
                response_data = {"message": "該LINE帳號已被註冊"}
            else:
                new_student = student(student_id=stdId, line_uid=LineUid, name=name, create_time=datetime.datetime.now())
                new_student.save()
        except:
            response_data = {"message": "發生未知錯誤"}
        return JsonResponse(response_data)
    
@csrf_exempt
def registerCard(request):
     if request.method == 'POST':
        card_id = request.POST.get('card_id')
        student = request.POST.get('student')
        toekn = request.POST.get('token')
        if toekn == "p+8bwe~s_74;`?%nq}#?t7~p7_rr6qe_&$?#@*ky//}f^!_b=&00852!sr:sz!a":
            req = card.addStudentCardId(student, card_id)
            return HttpResponse(req, status=200, content_type='text/plain')     
        return HttpResponse(f'error', status=200, content_type='text/plain')