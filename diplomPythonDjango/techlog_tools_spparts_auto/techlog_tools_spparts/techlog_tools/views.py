from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.http import HttpResponse
from .models import TechlogTools, TechlogTools2
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# from pprint import pprint
from django.contrib.auth.decorators import login_required


# Главная (домашняя) страница
def home(request):  # По умолчанию используется метод 'GET'
    tools = TechlogTools.objects.all()
    return render(request, "techlog_tools/home.html", {'tools': tools})


# Страница регистрации
def registr_user(request):
    if request.method == "GET":
        return render(request, 'techlog_tools/registration.html', {'form': UserCreationForm()})
    else:  # если метод "POST"
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


# Функция входа (авторизация пользователя)
def login_user(request):
    if request.method == "GET":
        return render(request, 'techlog_tools/loginuser.html', {'form': AuthenticationForm()})
    else:  # если метод "POST"
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'techlog_tools/loginuser.html',
                          {'form': AuthenticationForm(), 'error': "Неверные данные для входа"})
        else:
            login(request, user)
            return redirect('home')


# Функция выхода (закрыв сессию --> на главную стр.)
@login_required
def exitapp_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


# Функция страницы инструментов
@login_required
def techlog_tools(request):
    # Отсортируем по дате, для вывода последних сверху
    tltools2 = TechlogTools2.objects.order_by('-date')  # all()
    return render(request, 'techlog_tools/techtools.html', {
        'tltools2': tltools2,
    })


# для techlog_tools детализация
@login_required
def tool_details(request, techlog_tools_id):
    tool = get_object_or_404(TechlogTools2, pk=techlog_tools_id)
    return render(request, 'techlog_tools/tool_details.html',
                  {'tool': tool})
