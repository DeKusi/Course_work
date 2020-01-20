"""Course_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', views.home, name='home_url'),
    url(r'error/^$', views.error404),
    url(r'^registration/', views.registration, name='registration'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^account/', views.account, name='account'),
    url(r'^add_air/', views.add_air, name='add_air'),

    url(r'^user_list/', views.user_list),
    url(r'^moderator_list/', views.moderator_list),
    url(r'^add_user/', views.add_user, name='add_user'),
    url(r'^add_mod/', views.add_mod, name='add_mod'),
    url(r'^list_del_user/', views.list_del_user, name='list_del_user'),
    url(r'^list_del_mod/', views.list_del_mod, name='list_del_mod'),
    url(r'^airport/(?P<air_id>\d+)', views.air_detail, name='air_detail_url'),
    url(r'^del_user/(?P<user_id>\d+)', views.del_user1, name='del_user1'),
    url(r'^del_mod/(?P<mod_id>\d+)', views.del_mod1, name='del_mod1'),
    url(r'^add_ticket/(?P<air_id>\d+)/(?P<fly_id>\d+)', views.add_ticket, name='add_ticket')
]
