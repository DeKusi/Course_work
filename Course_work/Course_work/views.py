from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

import json


def home(request):
    with open("JSON/airports.json", 'rb') as read_file_json:
        airports = json.load(read_file_json)
        len_air = len(airports['airports'])
        num_cell = len_air + (len_air % 3)
        if len_air % 3 == 0:
            p = 0
        elif len_air % 3 == 1:
            p = 2
        elif len_air % 3 == 2:
            p = 1
        len_air_r = len_air + p
        air_list = []

        for i in range(0, len_air_r - 3, 3):
            rand_str = [airports['airports'][i], airports['airports'][i + 1], airports['airports'][i + 2]]
            air_list.append(rand_str)

        if p == 0:
            air_list.append([airports['airports'][len_air_r - 3], airports['airports'][len_air_r - 2],
                             airports['airports'][len_air_r - 1]])
        elif p == 1:
            air_list.append([airports['airports'][len_air_r - 3], airports['airports'][len_air_r - 2], 0])
        elif p == 2:
            air_list.append([airports['airports'][len_air_r - 3], 0, 0])
    return render(request, 'home.html', {'air_list': air_list})


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

    return render(request, 'login.html', {'form': logForm,
                                          'error': error})


def air_detail(request, air_id):
    with open("JSON/airports.json", encoding='utf-8') as read_file_json:
        air = json.load(read_file_json)

    name = air['airports'][int(air_id)-1]['name']
    flights = air['airports'][int(air_id)-1]['flights']

    return render(request, "air_detail.html", {"name": name, "flights": flights})
