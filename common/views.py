from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from common.forms import UserForm

def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
# 폼 인스턴스를 템플릿에 전달하여, 템플릿 내에서 폼의 필드들을 사용자가 볼 수 있게 함.