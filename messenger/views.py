from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Message
from account.models import Account

# Create your views here.

def admin_messenger(request):
    context = {'message_list' : Message.objects.all(), 'account_list' : Account.objects.all() }
    return render(request, 'admin/admin_messenger.html', context)

def individual_message(request, receiver_id):
    context = {}
    return render(request, 'admin/admin_messenger.html', context)

def help_message(request):
    context = {'message': "Message sent"}
    return render(request, 'home/contact_for_help.html', context)
