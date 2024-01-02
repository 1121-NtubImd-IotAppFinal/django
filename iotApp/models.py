import secrets
from django.db import models
import datetime
import requests


class student(models.Model):
    student_id = models.CharField(default="null", max_length=45, primary_key=True)
    line_uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=5)
    create_time = models.DateTimeField()

    @staticmethod
    def get_all_students():
        students = student.objects.values('student_id', 'name')
        return students
    
    @staticmethod
    def getStudentByLineUid(line_uid):
        student_instance = student.objects.get(line_uid=line_uid)
        return student_instance
    
    @staticmethod
    def studentIsRegister(line_uid):
        try:
            student.objects.get(line_uid=line_uid)
            return True 
        except student.DoesNotExist:
            return False

class sign(models.Model):
    sign_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    check_in_time = models.TimeField(default=None)
    check_out_time = models.TimeField(default=None, null=True)
    affair = models.TextField(default="", null=True)
    hours = models.FloatField()
    isLate = models.BooleanField()
    @staticmethod
    def studentTodayIsSign(student, today_date):
        try:
            sign_entry = sign.objects.filter(student=student, date=today_date, check_out_time=None).first()
            return sign_entry
        except sign.DoesNotExist:
            return None

    @staticmethod
    def getOrCreateSign(student):
        now = datetime.datetime.now()
        today_date = now.date()
        check_in = "out"
        sign_entry = sign.studentTodayIsSign(student, today_date)
        if(sign_entry == None or sign_entry.check_out_time != None):
            late_time = setting.objects.first().late_time
            sign_entry = sign(student=student, date=now, check_in_time=now, hours=0, isLate=now.time() > late_time)
            sign_entry.save()
            check_in = "in"
        else:
            start = sign_entry.check_in_time
            end = now.time()
            sign_entry.check_out_time = end
            start_minutes = start.hour * 60 + start.minute
            end_minutes = end.hour * 60 + end.minute
            minutes_difference = end_minutes - start_minutes            
            hours_difference = round(minutes_difference / 60, 2)
            sign_entry.hours = hours_difference
            sign_entry.save()
        formatted_date = now.strftime("%Y年%m月%d日 %H:%M:%S")
        return (sign_entry.sign_id, check_in, formatted_date, sign_entry.hours)

class image(models.Model):
    image_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=500)
    sign = models.ForeignKey(sign, on_delete=models.CASCADE)
    create_time = models.DateTimeField()

class card(models.Model):
    card_id = models.CharField(default="null", max_length=100, primary_key=True)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    create_time = models.DateTimeField()

    @staticmethod
    def addStudentCardId(student, newCard):
        now = datetime.datetime.now()
        card_count = card.objects.filter(student=student).count()
        if card_count > 10:
            return "exceed the limit"
        else:
            existing_card = card.objects.filter(card_id=newCard, student=student).first()
            if existing_card:
                return "already exists"
            else:
                card.objects.create(card_id=newCard, student_id=student, create_time=now)
                return "success"
    @staticmethod
    def deleteStudentCard(card_id):
        try:
            card_to_delete = card.objects.get(card_id=card_id)
            card_to_delete.delete()
            return "刪除成功"
        except:
            return "刪除失敗"
    @staticmethod
    def getStudentByCardId(card_id):
        try:
            card_object = card.objects.get(card_id=card_id)
            student = card_object.student
            return student
        except card.DoesNotExist:
            return None

class notify(models.Model):
    notify_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, unique=True)
    create_time = models.DateTimeField()

    @staticmethod
    def getTokenByStudent(studentId):
        student_instance = student.objects.get(student_id=studentId)
        try:
            notify_instance = notify.objects.get(student=student_instance)
            token = notify_instance.token
        except notify.DoesNotExist:
            token = None
        return token

    @staticmethod
    def userIsFind(studentId):
        try:
            notify.objects.get(student_id=studentId)
            return True
        except notify.DoesNotExist:
            return False

    @staticmethod
    def getNotifyToken(AuthorizeCode):
        body = {
            "grant_type": "authorization_code",
            "code": AuthorizeCode,
            "redirect_uri": "https://birc.leedong.work/notify",
            "client_id": "CN82GQa4zPRv2vaKU8BSr0",
            "client_secret": "SaYaAwYuL6XuAZZUTj5hghCEHlkAS25uDYH4EUvmI6w",
        }
        r = requests.post("https://notify-bot.line.me/oauth/token", data=body)
        response_data = r.json()
        token = response_data["access_token"]
        return token

    @staticmethod
    def lineNotifyMessage(token, msg):
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {"message": msg}
        requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, data=payload
        )
        return "successfully"

    @staticmethod
    def saveUserToken(token, student_id):
        now = datetime.datetime.now()
        if token == None:
            return False
        try:
            new_data = notify(student_id=student_id,token=token,create_time=now)
            new_data.save()
            return True
        except:
            return False
        
    @staticmethod
    def removeUser(studebt_id):
        notifications_to_delete = notify.objects.filter(student=studebt_id)
        notifications_to_delete.delete()

    @staticmethod
    def pustAllUser(msg):
        try:
            cursor = notify.objects.all()
            for obj in cursor:
                notify.lineNotifyMessage(obj.notify_token, msg)
            return "訊息成功發送"
        except:
            return "發送訊息時發生錯誤 !"

class setting(models.Model):
    hour_norm = models.IntegerField()
    late_time = models.TimeField()

class card_captcha(models.Model):
    captcha_sno = models.AutoField(primary_key=True)
    code_value = models.CharField(max_length=5, unique=True, editable=False)  # 添加 editable=False 避免手動編輯
    student = models.ForeignKey(student, on_delete=models.CASCADE)
    expiry_time = models.DateTimeField()
    create_time = models.DateTimeField()

    @staticmethod
    def createCode(student_id):
        now = datetime.datetime.now()
        expiry = now + datetime.timedelta(seconds=30)
        code_value = "#"+secrets.token_hex(3).upper()[:4]
        card_captcha_instance = card_captcha(student_id=student_id, code_value=code_value,expiry_time=expiry,create_time=now)
        card_captcha_instance.save()
        return (code_value,expiry.strftime("%Y-%m-%d %H:%M:%S"))
    
    @staticmethod
    def checkCode(student_id, code):
        now = datetime.datetime.now()
        latest_card_captcha = card_captcha.objects.filter(student_id=student_id, code_value=code).order_by('-create_time').first()
        if latest_card_captcha:
            if latest_card_captcha.expiry_time > now:
                return "驗證成功"
            else:
                return "驗證碼過期"
        else:
            return "驗證碼無效"
        
