from linebot.models import *
from django.db.models import Q,F
from iotApp.models import card, setting,sign
from iotApp.module.workdays import get_workdays
from ..module.encrypt import *
from django.utils import timezone
from django.db.models import Sum 
from ..module import encrypt


def notify_send(user_id, isFind):
    data = {}
    user_id = encrypt_string(user_id)
    find_url = f'https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=CN82GQa4zPRv2vaKU8BSr0&scope=notify&state={user_id}&redirect_uri=https://iotappdjango.leedong.work/notify'
    unfind_url = "https://notify-bot.line.me/"
    if(isFind):
        data = {"title":"移除通知綁定", "text":"請先登入LineNotify解除連動\n在按移除通知綁定移除資料\n若之後若要再綁定通知需重新設定"}
    else:
        data = {"title":"設定通知", "text":"即時訊息接收\n簽到簽退提醒通知"}

    find_uri_action = URIAction(
        label='點擊進行設定',
        uri=find_url
    )
    unfind_uri_action = URIAction(
        label='連接到LineNotify',
        uri=unfind_url
    )
    text_action = MessageAction(
        label='移除通知綁定',
        text='@移除通知綁定'
    )

    buttons_template = ButtonsTemplate(
        title=data["title"],
        text=data["text"],
        actions=[unfind_uri_action,text_action] if isFind else [find_uri_action]
    )
    template_message = TemplateSendMessage(
        alt_text='通知設定',
        template=buttons_template
    )
    return template_message

def card_send():
    data = {"title":"卡片設定", "text":"若要新增卡片請先攜帶您的卡片\n前往簽到退設備，然後再點擊下方的「新增卡片」按鈕"}
    addcard = MessageAction(
        label='新增卡片',
        text='@新增卡片'
    )    
    cardㄝList = MessageAction(
        label='管理卡片',
        text='@管理卡片'
    )
    buttons_template = ButtonsTemplate(
        title=data["title"],
        text=data["text"],
        actions=[addcard, cardㄝList]
    )
    template_message = TemplateSendMessage(
        alt_text='卡片設定',
        template=buttons_template
    )
    return template_message

def getCardListByStudent(student_id):
    cards = card.objects.filter(student_id=student_id)
    card_ids = [card.card_id for card in cards]
    message = ""
    if len(card_ids)==0:
        message = TextSendMessage(text="目前尚未綁定任何卡片")
    else:
        bubbles = []
        index = 0
        for card_id in card_ids:
            index +=1
            bubble = BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=f"卡片{index}:", weight='bold', size='xl'),
                        TextComponent(text=card_id, weight='bold', size='xl')
                    ]
                ),
                footer=BoxComponent(
                    layout='horizontal',
                    contents=[
                        ButtonComponent(
                            action=MessageAction(label='點擊刪除', text=f'@刪除卡片{card_id}')
                        )
                    ]
                )
            )
            bubbles.append(bubble)

        message = FlexSendMessage(alt_text='Card IDs', contents={
            "type": "carousel",
            "contents": bubbles
        })
    return message

def getSignListByStudent(student_id):
    signs = sign.objects.filter(student_id=student_id).order_by('-sign_id')
    signs = signs.filter(~Q(check_out_time=None))
    signs = [sign for sign in signs[:10]]
    message = ""
    if len(signs)==0:
        message = TextSendMessage(text="目前無任何簽到退紀錄")
    else:
        bubbles = []
        index = 0
        for sign_data in signs:
            signToken = encrypt.encrypt_string(str(sign_data.sign_id))
            index +=1
            bubble = BubbleContainer(
                direction='ltr',
                body=BoxComponent(
                    layout='vertical',
                    contents=[
                        TextComponent(text=f"{sign_data.date}", weight='bold', size='xl'),
                        TextComponent(text=f" ", weight='bold', size='xl'),
                        TextComponent(text=f"簽到時間: {sign_data.check_in_time.strftime('%H:%M')}", size='md'),
                        TextComponent(text=f"簽退時間: {sign_data.check_out_time.strftime('%H:%M')}", size='md'),
                        TextComponent(text=f" ", weight='bold', size='md'),
                        TextComponent(text=f"總計時數: {sign_data.hours}小時", weight='bold', size='md'),
                        TextComponent(text=f" ", weight='bold', size='md'),
                        TextComponent(text=f"進度回報狀態: {'尚未回報' if len(sign_data.affair)==0 else '已回報'}", weight='bold', size='sm'),
                    ]
                ),
                footer=BoxComponent(
                    layout='horizontal',
                    contents=[
                        ButtonComponent(
                            action=URIAction(label='點擊查看', uri=f'https://birc.leedong.work/report?token={signToken}') 
                        )
                    ]
                )
            )
            bubbles.append(bubble)

        message = FlexSendMessage(alt_text='Card IDs', contents={
            "type": "carousel",
            "contents": bubbles
        })
    return message

def getLackHour(student_instance):
    current_datetime = timezone.now().date()
    student_instance.create_time = student_instance.create_time.date()
    hourNorm = setting.objects.first().hour_norm
    workdays = get_workdays(student_instance.create_time, current_datetime)
    X = workdays * hourNorm
    Y = sign.objects.filter(student=student_instance).aggregate(total_hours=Sum('hours'))['total_hours']
    missing_hours = round(X - Y if Y is not None else X,2)
    Y = round(Y,2) if Y is not None else 0.0
    req = f"您的時數計算日期為: {student_instance.create_time}\n至 {current_datetime}\n"
    req += f"\n在此之間經過了 {workdays}天\n(備註: 不含六日)\n"
    req += f"\n因此您應到達的\n時數為 {X}小時"
    req += f"\n(公式: {workdays} * {hourNorm} = {X})\n"
    req += f"\n您在此段時間裡\n一共累積了 {Y}小時\n"
    req += f"\n目前您所欠缺的時數為 {missing_hours}小時"
    return req