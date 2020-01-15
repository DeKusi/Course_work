from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

import json


def home(request):
    return render(request, 'home.html', {})


def account(request):
    page = 'account.html'
    if "id" not in request.session:
        page = "error_404.html"
    return render(request, page, {})


def login(request):
    logForm = LoginForm(request.POST or None)
    error = 'None'
    if 'id' in request:
        return redirect("/account")
    if request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        # Проверка входа в систему
        checkLogin = req.get("login")
        checkPass = req.get("password")
        error = 'Неправильно введён логин или пароль'
 #       checkFunc = "none"
        for user in users['users']:
            if user['login'] == checkLogin and user['password'] == checkPass:
                request.session.set_expiry(15)
                request.session['id'] = user['id']
                request.session['login'] = user['login']
                request.session['position'] = user['position']
                return redirect("/account")
            break

    return render(request, 'login.html', {'form': logForm,
                                          'error': error})
