from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def messenger(request):
    context = {}
    return render(request, 'admin/admin_messenger.html', context)

def entity_list(request):
    context = {}
    return render(request, 'admin/admin_messenger.html', context)

def admin_home(request):
    context = {}
    return render(request, 'admin/admin_home.html', context)

def create_admin(request):
    context = {}
    return render(request, 'admin/admin_home.html', context)
