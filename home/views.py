from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from account.models import Account
from user_ver import user_ver
from entity.models import Entity

# Create your views here.       HOME VIEW


def home(request):
    user_ver(request, False)
    context = {'username': Account.objects.get(id=request.session['user_id']).username, 'recommend_list': Entity.objects.all().order_by("-positive_review")[:4]}
    return render(request, 'home/home.html', context)

def support(request):
    user_ver(request, False)
    return render(request, 'home/contact_for_help.html')

# ADMIN
def admin_home(request):
    user_ver(request, True)
    context = {'ac': Account.objects.get(id = request.session['user_id'])}
    return render(request, 'admin/admin_home.html', context)

