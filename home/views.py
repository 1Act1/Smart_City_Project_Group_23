from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from account.models import Account
from user_ver import user_ver
from entity.models import Entity

# Create your views here.       HOME VIEW


def home(request):
    user_ver(request, False)
    ac = Account.objects.get(id=request.session['user_id'])
    if ac.account_type == 'Student' :
        recommend_list = Entity.objects.all().order_by("-positive_review").exclude(type='Hotel').exclude(type='Industry')[:4]
    if ac.account_type == 'Tourist' :
        recommend_list = Entity.objects.all().order_by("-positive_review").exclude(type='College').exclude(type='Industry').exclude(type='Library')[:4]
    if ac.account_type == 'Businessman' :
        recommend_list = Entity.objects.all().order_by("-positive_review").exclude(type='College').exclude(type='Library')[:4]
    context = {'username': ac.username, 'recommend_list': recommend_list}
    return render(request, 'home/home.html', context)

def support(request):
    user_ver(request, False)
    return render(request, 'home/contact_for_help.html')

# ADMIN
def admin_home(request):
    user_ver(request, True)
    context = {'ac': Account.objects.get(id = request.session['user_id'])}
    return render(request, 'admin/admin_home.html', context)

