from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Question

def index(request):
    page = request.GET.get('page','1')
    #GET 방식으로 호출된 url에서 page값 가져올 때 사용함. 'pybo1/' 처럼 page값 없이 호출되면 디폴트 값인 1이 호출됨
    kw = request.GET.get('kw', '')  # 검색어
    question_list = Question.objects.order_by('-create_date') #objects?
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10) #페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page) # 'page_obj' : 페이징객체. 점투장 참고
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    #뷰에서 템플릿으로 데이터 전달 위해 씀
    return render(request, 'pybo1/question_list.html',context)

def detail(request, question_id):
    question =get_object_or_404(Question, pk=question_id) #Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo1/question_detail.html',context)