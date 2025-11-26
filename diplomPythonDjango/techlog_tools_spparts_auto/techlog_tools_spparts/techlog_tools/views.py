from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request):  # Пол умолчанию используется метод 'GET'
    return render(request, "techlog_tools/home.html", {"password": "qwerty"})


def registr_user(request):
    if request.method == "GET":
        return render(request, 'techlog_tools/registration.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'techlog_tools/registration.html',
                              {'form': UserCreationForm(),
                               'error': 'Данное имя пользователя уже существует. Задайте другое.'})
        else:
            return render(request, 'techlog_tools/registration.html',
                          {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})


def exitapp_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def login_user(request):
    if request.method == "GET":
        return render(request, 'techlog_tools/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'techlog_tools/loginuser.html',
                          {'form': AuthenticationForm(), 'error': "Неверные данные для входа"})
        else:
            login(request, user)
            return redirect('home')
