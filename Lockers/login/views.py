from django.shortcuts import render , redirect
from django.urls import reverse
from .models import User

from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreateForm

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def create(request):
    if request.method == 'GET':
        return render(
            request,
            "login/create.html",
            {"form":CustomUserCreateForm()}
        )
    elif request.method == "POST":
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(reverse('home'))
        else:
            return render(request, "login/create.html",{"form":form})

def user_login(request):
    if request.method == "GET":
        return render(request,
                      'login/login.html',
                      {'form':AuthenticationForm()})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username , password=password)
        if user is not None :
            login(request, user)
            return redirect(reverse('login:loginhome'))
        else :
            return render(
                request,
                'login/login.html',
                {'form': AuthenticationForm(),
                "errorMessage":"ID나 Password를 다시 확인하세요."}
            )
        
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("home"))

@login_required
def loginhome(request):
    if request.method =="GET":
        return render(request,'login/loginhome.html')

@login_required
def user_update(request):
    if request.method == "GET":
        form = CustomUserChangeForm(instance = request.user)
        return render(request, "login/update.html", {"form":form})
    elif request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request , user)
            return redirect(reverse('login:detail'))
        else:
            return render(request, "login/update.html", {"from" : form})
@login_required
def detail(request):
    user = User.objects.get(pk=request.user.pk)
    return render(request, "login/detail.html", {"object":user})

from django.contrib import messages
from .forms import CustomUserChangeForm, CustomPasswordChangeForm

@login_required
def change_password(request):
    if request.method == "GET":
        form = CustomPasswordChangeForm(request.user)
        return render(
            request , "login/password_change.html",
            {"form":form}
        )
    elif request.method == "POST":
        form = CustomPasswordChangeForm(request.user , request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse("login:detail"))
        else :
            return render(
                request , 'login/password_change.html',
                {'form':form  , 'errorMessage' : '패스워드를 다시 입력하세요.'}
            )


#######id 찾기 ###########
from .forms import RecoveryIdForm
from django.views.generic import View


class RecoveryIdView(View):
    template_name = 'login/user_base.html'
    form_class = RecoveryIdForm

    def get(self, request):
        if request.method=='GET':
            form = self.form_class(None)
        return render(request, self.template_name, { 'form':form, })

from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import User


def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    result_id = User.objects.get(name=name, email=email)
       
    return HttpResponse(json.dumps({"result_id": result_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")
