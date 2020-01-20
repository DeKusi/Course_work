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
    with open("JSON/users.json", 'rb') as read_file_json:
        users = json.load(read_file_json)
    page = 'account.html'
    if "id" not in request.session or request.session['status'] == 'false':
        page = "error_404.html"
    elif request.session['position'] == 'user':
        page = 'account_user.html'
    elif request.session['position'] == 'admin':
        page = 'account_admin.html'
    elif request.session['position'] == 'moderator':
        page = 'account_moderator.html'

    # Проверка, покупал ли билеты
    if len(users['users'][int(request.session['id']) - 1]['tickets']) == 0:
        data = [0]
    else:
        data = users['users'][int(request.session['id']) - 1]['tickets']
    return render(request, page, {'data': data})


def error404(request):
    return render(request, 'error_404.html', {})


def add_air(request):
    AddForm = AddAir(request.POST or None)
    error = 'None'
    if request.session['position'] != 'admin':
        return redirect("/error")
    elif request.POST:
        with open("JSON/airports.json", 'rb') as read_file_json:
            airports = json.load(read_file_json)
        req = request.POST
        name = req.get("name")
        for air in airports['airports']:
            if air['name'] == name:
                error = 'Аэропорт уже есть'
        if error == 'None':
            airports['airports'].append({"name": name,
                                         "id": len(airports['airports']) + 1,
                                         "flights": []})
            with open('JSON/airports.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(airports, ensure_ascii=False, separators=(',', ': '), indent=2))
            id1 = str(airports['airports'][-1]['id'])
            urlre = '/airport/' + id1
            return redirect(urlre)

    return render(request, "add_air.html", {'form': AddForm,
                                            'error': error})


def user_list(request):
    if "id" not in request.session or request.session['status'] == 'false':
        return redirect("/error")
    else:
        with open("JSON/users.json", encoding='utf-8') as read_file_json:
            users = json.load(read_file_json)
        data = users['users']
    return render(request, "user_list.html", {'data': data})


def moderator_list(request):
    if "id" not in request.session or request.session['status'] == 'false':
        return redirect("/error")
    else:
        with open("JSON/users.json", encoding='utf-8') as read_file_json:
            users = json.load(read_file_json)
        data = users['users']
    return render(request, "moderator_list.html", {'data': data})


def add_user(request):
    AddForm = AddUser(request.POST or None)
    error = 'None'
    if request.session['position'] != 'admin' and request.session['position'] != 'moderator':
        return redirect("/error")
    elif request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        Login = req.get("login")
        Pass = req.get("password")

        for user in users['users']:
            if user['login'] == Login:
                error = 'Пользователь уже зрегистрирован'

        if error == 'None':
            users['users'].append({"login": Login,
                                   "id": len(users['users']) + 1,
                                   "password": Pass,
                                   "position": "user",
                                   "status": "true",
                                   "tickets": []})
            with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))

            return redirect("/user_list")

    return render(request, "add_user.html", {'form': AddForm,
                                             'error': error})


def add_mod(request):
    AddForm = AddMod(request.POST or None)
    error = 'None'
    if 'id' not in request.session:
        return redirect("/error")
    elif request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        Login = req.get("login")
        Pass = req.get("password")

        for user in users['users']:
            if user['login'] == Login:
                error = 'Пользователь уже зрегистрирован'

        if error == 'None':
            users['users'].append({"login": Login,
                                   "id": len(users['users']) + 1,
                                   "password": Pass,
                                   "position": "moderator",
                                   "status": "true",
                                   "tickets": []})
            with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))
            return redirect("/moderator_list")

    return render(request, "add_mod.html", {'form': AddForm,
                                            'error': error})


def list_del_user(request):
    if request.session['position'] != 'admin' and request.session['position'] != 'moderator' or request.session[
        'status'] == 'false':
        return redirect("/error")
    else:
        with open("JSON/users.json", encoding='utf-8') as read_file_json:
            users = json.load(read_file_json)
        data = users['users']
    return render(request, "del_user.html", {'data': data})


def list_del_mod(request):
    if request.session['position'] != 'admin' or request.session['status'] == 'false':
        return redirect("/error")
    else:
        with open("JSON/users.json", encoding='utf-8') as read_file_json:
            users = json.load(read_file_json)
        data = users['users']
    return render(request, "del_mod.html", {'data': data})


def del_user1(request, user_id):
    if request.session['position'] != 'admin' and request.session['position'] != 'moderator' or request.session[
        'status'] == 'false':
        return redirect("/error")
    with open("JSON/users.json", encoding='utf-8') as read_file_json:
        users = json.load(read_file_json)
    users['users'][int(user_id) - 1]['status'] = 'false'
    with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
        read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))
    return redirect("/list_del_user")


def del_mod1(request, mod_id):
    if request.session['position'] != 'admin' or request.session['status'] == 'false':
        return redirect("/error")
    with open("JSON/users.json", encoding='utf-8') as read_file_json:
        users = json.load(read_file_json)
    users['users'][int(mod_id) - 1]['status'] = 'false'
    with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
        read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))
    return redirect("/list_del_mod")


def registration(request):
    AddForm = AddUser(request.POST or None)
    error = 'None'
    if request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        Login = req.get("login")
        Pass = req.get("password")

        for user in users['users']:
            if user['login'] == Login:
                error = 'Пользователь уже зрегистрирован'

        if error == 'None':
            users['users'].append({"login": Login,
                                   "id": len(users['users']) + 1,
                                   "password": Pass,
                                   "position": "user",
                                   "status": "true",
                                   "tickets": []})
            with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
                read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))
            request.session.set_expiry(86400)
            request.session['id'] = users['users'][-1]['id']
            request.session['login'] = users['users'][-1]['login']
            request.session['position'] = users['users'][-1]['position']
            request.session['status'] = users['users'][-1]['status']
            return redirect("/account")
    return render(request, "registration.html", {'form': AddForm,
                                                 'error': error})


def login(request):
    logForm = LoginForm(request.POST or None)
    error = 'None'
    if 'id' in request:
        return redirect("/error")
    if request.POST:
        with open("JSON/users.json", 'rb') as read_file_json:
            users = json.load(read_file_json)
        req = request.POST
        # Проверка входа в систему
        Login = req.get("login")
        Pass = req.get("password")
        error = 'Неправильно введён логин или пароль'
        #       checkFunc = "none"
        for user in users['users']:
            if user['login'] == Login and user['password'] == Pass and user['status'] == 'true':
                request.session.set_expiry(86400)
                request.session['id'] = user['id']
                request.session['login'] = user['login']
                request.session['position'] = user['position']
                request.session['status'] = user['status']
                return redirect("/account")

    return render(request, 'login.html', {'form': logForm,
                                          'error': error})


def logout(request):
    request.session.clear()
    return redirect("/")


def air_detail(request, air_id):
    list_point_of_departure = []
    user_tickets = 0
    with open("JSON/airports.json", encoding='utf-8') as read_file_json:
        air = json.load(read_file_json)

    name = air['airports'][int(air_id) - 1]['name']
    id = air_id
    if len(air['airports'][int(air_id) - 1]['flights']) == 0:
        flights = 0
    else:
        flights = air['airports'][int(air_id) - 1]['flights']

    # если зареганный чел, то если куплен билет, на кнопочке писалось куплен
    if 'id' in request.session:
        with open("JSON/users.json", encoding='utf-8') as read_file_json:
            users = json.load(read_file_json)
        user_tickets = users['users'][int(request.session['id']) - 1]['tickets']
        list_fly_id = []
        for tik in user_tickets:
            list_point_of_departure.append(tik['point_of_departure'])

    return render(request, "air_detail.html", {"name": name,
                                               "id": id,
                                               "flights": flights,
                                               "user_tickets": user_tickets,
                                               'list_point_of_departure': list_point_of_departure})


def add_ticket(request, air_id, fly_id):
    with open("JSON/users.json", encoding='utf-8') as read_file_json:
        users = json.load(read_file_json)
    with open("JSON/airports.json", encoding='utf-8') as read_file_air_json:
        airports = json.load(read_file_air_json)

    users['users'][int(request.session['id']) - 1]['tickets'].append(
        airports['airports'][int(air_id) - 1]['flights'][int(fly_id) - 1])

    with open('JSON/users.json', 'w', encoding='utf-8') as read_file_json:
        read_file_json.write(json.dumps(users, ensure_ascii=False, separators=(',', ': '), indent=2))

    return redirect("/account")
