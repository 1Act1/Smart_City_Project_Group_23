from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from account.models import Account

def user_ver(request):
    try:
        request.session[user_id]
    except KeyError:
        return Http404("Unknown user")

# Create your views here.       HOME VIEW


def home(request):
    user_ver(request)
    context = {'username': Account.objects.get(id=request.session['user_id']).username}
    return render(request, 'home/home.html', context)

def support(request):
    user_ver(request)
    return render(request, 'home/contact_for_help.html')

# ADMIN
def admin_home(request):
    user_ver(request)
    context = {}
    return render(request, 'admin/admin_home.html', context)

