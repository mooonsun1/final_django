from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , PasswordChangeForm

from .models import User

class CustomUserCreateForm(UserCreationForm):
    
    password1 = forms.CharField(label='비밀번호' , widget=forms.PasswordInput())
    password2 = forms.CharField(label="비밀번호 확인",
                                widget=forms.PasswordInput(),
                                help_text="비밀번호 확인을 위해 이전과 동일한 비밀번호를 입력하세요.")
    phone = forms.CharField(label="전화번호" , help_text="'-'는 빼고 입력하세요")
    
    class Meta:
        model = User
        fields =['username','password1','password2','name','email','phone']

from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()

# 사용자 정보 및 비밀번호 변경 폼
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="기존 패스워드",
        widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        label="새 패스워드",
        widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        label="새 패스워드 확인",
        widget=forms.PasswordInput()
    )

class RecoveryIdForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput,)
    email = forms.EmailField(widget=forms.EmailInput,)

    class Meta:
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(RecoveryIdForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '이름'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_name',
        })
        self.fields['email'].label = '이메일'
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'id': 'form_email' 
        })