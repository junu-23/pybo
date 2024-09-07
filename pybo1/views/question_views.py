from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    # POST 요청일 때, 폼 데이터를 처리하고 저장
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo1:index')
    else:
        # GET 요청일 때, 빈 폼을 생성하여 렌더링
        form = QuestionForm()
        # 폼 클래스의 인스터스 -> 질문작성 기본 틀 제공
    context = {'form': form}
    return render(request, 'pybo1/question_form.html', context)
    # render 함수는 지정된 템플릿과 컨텍스트를 html로 반환함.

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo1:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False) #commit=False : 저장할 내용이 남았기 때문
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo1:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
        #폼 생성시 instance 값을 지정하면 폼의 속성 값이 instance값으로 채워짐
        #따라서 질문을 수정하는 화면에서 제목과 내용이 채워진 채로 보인다.
    context = {'form': form}
    return render(request, 'pybo1/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: #작성자와 사용자가 다르면
        messages.error(request, '삭제권한이 없습니다.') # 이 메시지 띄워주고
        return redirect('pybo1:detail',question_id=question.id) # 여기로 보낸다.
    question.delete() # 작성자와 사용자가 같으면
    return redirect('pybo1:index') #여기로 보낸다.

@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo1:detail', question_id=question.id)











