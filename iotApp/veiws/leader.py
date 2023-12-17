from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from iotApp.middleware import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            return render(request, 'leader/login.html', {'error': '使用者名稱或密碼錯誤'})
    else:
        return render(request, 'leader/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


