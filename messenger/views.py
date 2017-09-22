from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Message
from account.models import Account
from user_ver import user_ver
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.              MESSENGER VIEW

def admin_messenger(request):
    user_ver(request, True)
    admin_id = request.session['user_id']
    
    x = []
    message_list = Message.objects.all()
    sender = False
    
    for message in message_list:
        if message.receiverid != admin_id and message.senderid != admin_id:
            message_list.exclude(id = message.id)
        else:
            if message.receiverid != admin_id:
                if message.receiverid not in x:
                    x.append(message.receiverid)
                else:
                    message_list.exclude(id = message.id)
            else:
                if message.senderid not in x:
                    x.append(message.senderid)
                else:
                    message_list.exclude(id = message.id)

    context = {'conversation_list': x, 'account_list' : Account.objects.all() }
    return render(request, 'admin/admin_messenger.html', context)

def conversation(request, receiver_id):
    user_ver(request, True)
    x = []
    admin_id = request.session['user_id']
    messages = Message.objects.order_by('deliver_date', 'deliver_time').all()
    for each in messages:
        if ((int(each.receiverid) == int(receiver_id)) and (int(each.senderid) == int(admin_id))):
            x.append(each)
        if ((int(each.receiverid) == int(admin_id)) and (int(each.senderid) == int(receiver_id))):
            x.append(each)
        #if (not (((each.receiverid == receiver_id) and (each.senderid == admin_id))or ((each.receiverid == admin_id) and (each.senderid == receiver_id)))):
    
    #messages.exclude(id = each.id)

    context = {'messages': x, 'account_list': Account.objects.all(), 'receiver_id': int(receiver_id)}
    return render(request, 'admin/admin_conversation.html', context)

def add_message(request, receiver_id):
    user_ver(request, True)
    
    my_message = request.POST['conversationbox']
    
    if my_message != "":
        a = Message(senderid = request.session['user_id'], receiverid = receiver_id, message = my_message)
        a.save()
    
    return HttpResponseRedirect(reverse('adminconversation', args=(receiver_id,)))


def start_new_conversation(request):
    user_ver(request, True)
    context = {'ac': Account.objects.all(), 'myac': Account.objects.get(id = request.session['user_id'])}
    return render(request, 'admin/admin_start_new_conversation.html', context)

def create_conversation(request, receiver_id):
    user_ver(request, True)
    return HttpResponseRedirect(reverse('adminconversation', args=(receiver_id,)))

def help_message(request):
    user_ver(request, False)
    
    receiving_admin = Account.objects.get(username = 'susan')
    help_message = request.POST['help box']
    
    a = Message(senderid = request.session['user_id'], receiverid = receiving_admin.id, message = help_message)
    a.save()
    
    context = {'message': "Message sent"}
    return render(request, 'home/contact_for_help.html', context)
