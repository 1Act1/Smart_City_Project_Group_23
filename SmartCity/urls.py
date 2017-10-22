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
from messenger import views as msviews

namespace = 'Smartcity'

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
        
    #hmviews
    url(r'^home/$', hmviews.home, name = 'userhome'),
    url(r'^home/support/$', hmviews.support, name = 'support'),
    url(r'^adminhome/$', hmviews.admin_home, name = 'adminhome'),
               
    
    #acviews
    url(r'^$', acviews.login, name = 'login'),
    url(r'^logout/$', acviews.logout, name = 'logout'),
    url(r'^loginver$', acviews.loginver, name = 'loginver'),
    url(r'^createac/$', acviews.createac, name = 'createac'),
    url(r'^createprocess/$', acviews.createprocess, name = 'createprocess'),
    url(r'^createadminprocess/$', acviews.createadminprocess, name = 'createadminprocess'),
    url(r'^editacdetail/$', acviews.editac, name = 'editac'),
    url(r'^editacdetail/save/$', acviews.editacsave, name = 'editacsave'),
    url(r'^adminhome/createadmin/$', acviews.createadmin, name = 'createadmin'),
    url(r'^recoverac/$', acviews.recoverac, name = 'recoverac'),
    url(r'^recoverac/username/$', acviews.recoverusername, name = 'recoverusername'),
    url(r'^recoverac/password/$', acviews.recoverpassword, name = 'recoverpassword'),
    url(r'^recoverac/password/confirm/$', acviews.recoverpasswordconfirm, name = 'recoverpasswordconfirm'),
    
    #enviews
    url(r'^home/entitylist/$', enviews.list, name = 'list'),
    url(r'^home/entitylist/(?P<entity_id>[0-9]+)/$', enviews.detail, name = 'detail'),
    url(r'^home/entitylist/(?P<entity_id>[0-9]+)/review/$', enviews.review, name = 'review'),
    url(r'^home/entitylist/search/$', enviews.search, name = 'search'),
    url(r'^adminhome/entitylist/$', enviews.admin_entity_list, name = 'adminentitylist'),
    url(r'^adminhome/entitylist/(?P<entity_id>[0-9]+)/$', enviews.edit_entity, name = 'editentity'),
    url(r'^adminhome/entitylist/(?P<entity_id>[0-9]+)/draft/$', enviews.draft, name = 'editentitydraft'),
    url(r'^adminhome/entitylist/(?P<entity_id>[0-9]+)/save/$', enviews.edit_entity_save, name = 'editentitysave'),
    url(r'^adminhome/entitylist/search/$', enviews.adminsearch, name = 'adminsearch'),
            
    #msview
    url(r'^home/support/sent/$', msviews.help_message, name = 'helpmessage'),
    url(r'^home/support/messenger/$', msviews.user_messenger, name = 'usermessenger'),
    url(r'^home/support/messenger/(?P<receiver_id>[0-9]+)/$', msviews.conversation, name = 'userconversation'),
    url(r'^adminhome/messenger/$', msviews.admin_messenger, name = 'adminmessenger'),
    url(r'^adminhome/messenger/(?P<receiver_id>[0-9]+)/$', msviews.conversation, name = 'adminconversation'),
    url(r'^adminhome/messenger/(?P<receiver_id>[0-9]+)/add/$', msviews.add_message, name = 'add_message'),
    url(r'^adminhome/messenger/startnew/$', msviews.start_new_conversation, name = 'startnewconversation'),
    url(r'^adminhome/messenger/startnew/create/(?P<receiver_id>[0-9]+)/$', msviews.create_conversation, name = 'createconversation'),
               
               
    
    
    
               
               
]














# eof
