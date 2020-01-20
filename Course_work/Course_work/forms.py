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

