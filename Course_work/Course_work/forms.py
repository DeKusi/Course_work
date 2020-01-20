from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пароль ", widget=forms.PasswordInput())


class AddUser(forms.Form):
    login = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пароль ", widget=forms.PasswordInput())


class AddMod(forms.Form):
    login = forms.CharField(label="Логин ", max_length=100)
    password = forms.CharField(label="Пароль ", widget=forms.PasswordInput())


class AddAir(forms.Form):
    name = forms.CharField(label="Название ", max_length=100)


class AddFly(forms.Form):
    surf_point = forms.CharField(label="Пункт прибытия ", max_length=100)
    departure_time = forms.CharField(label="Время отбытия ", max_length=100)
    arrival_time = forms.CharField(label="Время прибытия ", max_length=100)
    plane_name = forms.CharField(label="Название самолёта ", max_length=100)
    plane_model = forms.CharField(label="Модель самолёта ", max_length=100)
    plane_type = forms.CharField(label="Тип самолёта ", max_length=100)
    service_classes = forms.CharField(label="Классы обслуживания(через ,) ", max_length=100)
