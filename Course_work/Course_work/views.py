from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.views.decorators.csrf import csrf_exempt

import json


def login(request):
    logForm = LoginForm(request.POST or None)
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
            if user['login'] == checkLogin and user['password'] == checkPass:
                request.session.set_expiry(86400)
                request.session['in'] = True
                request.session['login'] = user['login']
                request.session['position'] = user['position']
                page = "account.html"
                break
    return render(request, page, {'form': logForm})
