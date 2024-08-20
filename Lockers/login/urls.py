from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

app_name="login"

urlpatterns = [
    path("create/", views.create, name="create"),  # 회원가입
    path("login/",views.user_login,name="login"),  # 로그인
    path("loginhome/", views.loginhome, name="loginhome"), # 로그인 후 홈화면
    path("detail/" , views.detail , name='detail'),  # 회원정보 조회
    path("update/" , views.user_update , name='update'), # 회원정보수정
    path("password_change/" ,views.change_password , name="password_change"), # 비밀번호변경
    path('user_base/', views.RecoveryIdView.as_view(), name='user_base'),  # 아이디 찾기
    path('id/find/', views.ajax_find_id_view, name='ajax_id'), 

]