from django import forms
from pybo1.models import Question, Answer

class QuestionForm(forms.ModelForm): #질문 등록시 사용할 Question폼
    class Meta:
        model = Question #사용할 모델
        fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성
        #모델 폼은 모델과 연결된 폼으로, 폼을 저장하면 연결된 모델의 데이터 저장 가능
        labels = { #레이블 쓰는 이유?
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용', # 뒤에 콤마 왜 찍나?
        }