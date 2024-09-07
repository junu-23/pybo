from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    pybo1 답변등록
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user # author 속성에 로그인 계정 저장
            answer.create_date=timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
        #question_id=question.id
        #answer.question = question  ???
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo1/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo1:detail', question_id=answer.question.id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=answer.question.id), answer.id))
    else: #get일때 수정할 답변의 기존 데이터 포함 폼을 생성해 사용자에게 보여줌->
        #사용자는 이 폼으로 답변 수정 가능
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo1/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권이 없습니다.')
    else:
        answer.delete()
    return redirect('pybo1:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_vote(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=answer.question.id), answer.id))