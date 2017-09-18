"""SmartCity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from account import views as acviews
from home import views as hmviews
from entity import views as enviews
from scadmin import views as adviews

namespace = 'Smartcity'

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
        
    #hmviews
    url(r'^home/$', hmviews.home, name = 'home'),
    url(r'^home/support/$', hmviews.support, name = 'support'),
               
    
    #acviews
    url(r'^$', acviews.login, name = 'login'),
    url(r'^loginver$', acviews.loginver, name = 'loginver'),
    url(r'^createac/$', acviews.createac, name = 'createac'),
    url(r'^createprocess/$', acviews.createprocess, name = 'createprocess'),
    url(r'^editacdetail/$', acviews.editac, name = 'editac'),
    
    #enviews
    url(r'^home/entitylist/$', enviews.list, name = 'list'),
    url(r'^home/entitylist/(?P<entity_id>[0-9]+)/$', enviews.detail, name = 'detail'),
    url(r'^home/entitylist/(?P<entity_id>[0-9]+)/review/$', enviews.review, name = 'review'),
               
    #admin
    url(r'^adminhome/$', adviews.admin_home, name = 'adminhome'),
    url(r'^adminhome/messenger/$', adviews.messenger, name = 'adminmessenger'),
    url(r'^adminhome/entitylist/$', adviews.entity_list, name = 'adminentitylist'),
    url(r'^adminhome/createadmin/$', adviews.create_admin, name = 'createadmin'),
    
]














# eof
