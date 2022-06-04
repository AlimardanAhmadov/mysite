from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import activate
activate('tr')
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-solid'}), max_length=32)
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-solid'}), max_length=32, help_text='Last name')
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg form-control-solid' }), max_length=64, help_text='Enter a valid email address')
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg form-control-solid'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg form-control-solid'}))
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password1","password2"]

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg form-control-solid' }), max_length=64, help_text='Enter a valid email address')
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg form-control-solid'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
            print(user)
            if not user:
                raise forms.ValidationError("User does not exist.")
        return super(LoginForm, self).clean(*args, **kwargs)