from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

User = get_user_model()
# Create your views here.

def register(response):
    
    form = CreateUserForm()
    if response.method=="POST":
        form = CreateUserForm(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    context = {"form":form}
    return render(response, "register/register.html", context)    

def view_login(response):
    if response.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if response.method == 'POST':
            email = response.POST.get('email')
            password = response.POST.get('password')
            user = authenticate(response, email=email, password=password)
            if user is not None:
                login(response,user)
                return HttpResponseRedirect('/')
            else:
                messages.info(response, 'Try again! username or password is incorrect')
        context = {}
    return render(response, "register/login.html", context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')
    
    