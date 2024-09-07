#Django 프로젝트 전체의 URL 설정을 관리하는 파일
from django.contrib import admin
from django.urls import include, path
from pybo1.views import base_views

urlpatterns = [
    path('pybo1/', include('pybo1.urls')),
    path('common/', include('common.urls')),
    path('admin/', admin.site.urls),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path
]
