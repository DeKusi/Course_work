from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.views.decorators.csrf import csrf_exempt

import json


def home(request):
    return render(request, 'home.html', {})

def account(request):
    page = 'account.html'
    if "in" not in request.session:
        page = "error_404.html"
    return render(request, page, {})

def login(request):
    logForm = LoginForm(request.POST or None)
    dict1 = {}
    page = "login.html"
    if request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        # Проверка входа в систему
        checkLogin = req.get("login")
        checkPass = req.get("password")
        checkFunc = "none"
        for user in users['users']:
            if ('in' is request):
                page = 'vi_uje_avtorizovan.html'
            elif user['login'] == checkLogin and user['password'] == checkPass:
                request.session.set_expiry(15)
                request.session['in'] = True
                request.session['login'] = user['login']
                request.session['position'] = user['position']
                page = "account.html"
                dict1 = {'login': user['login'],
                         'id': user['id'],
                         'position': user['position']}
                break
    return render(request, page, {'form': logForm,
                                  'dict': dict1})
