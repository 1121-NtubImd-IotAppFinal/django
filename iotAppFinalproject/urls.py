"""
URL configuration for iotAppFinalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from iotApp.veiws import linebot,leader,searchHour,notify,sign, later, hours, \
    manager, set_time,people,card

urlpatterns = [
    path('linebot', linebot.line_bot_webhook),
    path('linebot/send', linebot.handle_message),
    path('linebot/register', linebot.register, name="register"),
    path('', searchHour.frontend, name='main'),
    path('cardCheck',sign.cardCheck),
    path('login', leader.login_view, name='login'),
    path('logout', leader.logout_view, name='logout'),
    path('later', later.later, name='later'),
    path('hours', hours.hours, name='hours'),
    path('notify', notify.userBind),
    path('sign', sign.image_check),
    path('report', sign.report),
    path('upload', sign.saveImage),
    path('reportUrl', sign.getReportUrl),
    path('registerCard', linebot.registerCard),
    path('set_time', set_time.set_time, name='set_time'),
    path('manager', manager.manager, name='manager'),
    path('people', people.people, name='people'),
    path('cardman', card.cardman, name='cardman'),   
    path('card/delete/<str:card_id>/', card.delete_card, name='delete_card'),
    path('delete_student/<str:student_id>/', people.delete_student, name='delete_student')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
