from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Message
from account.models import Account
from user_ver import user_ver
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.              MESSENGER VIEW

def user_messenger(request):
    user_ver(request, False)
    admin_id = request.session['user_id']
    
    x = []
    message_list = Message.objects.all()
    
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

    context = {'conversation_list': x, 'account_list' : Account.objects.all(), 'admin': False }
    return render(request, 'messenger/messenger.html', context)

def admin_messenger(request):
    user_ver(request, True)
    admin_id = request.session['user_id']
    
    x = []
    message_list = Message.objects.all()
    #sender = False
    
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

    context = {'conversation_list': x, 'account_list' : Account.objects.all(), 'admin': True }
    return render(request, 'messenger/messenger.html', context)

def conversation(request, receiver_id):
    user_ver(request, False, True)
    x = []
    count = 0
    admin_id = request.session['user_id']
    messages = Message.objects.order_by('deliver_date', 'deliver_time').all()
    for each in messages:
        if ((int(each.receiverid) == int(receiver_id)) and (int(each.senderid) == int(admin_id))):
            x.append(each)
            count += 1
        if ((int(each.receiverid) == int(admin_id)) and (int(each.senderid) == int(receiver_id))):
            x.append(each)
            count += 1

    if Account.objects.get(id = request.session['user_id']).account_type == "Admin":
        admin = True
    else:
        admin = False
    context = {'messages': x, 'account_list': Account.objects.all(), 'receiver_id': int(receiver_id), 'admin': admin, 'count': count}
    return render(request, 'messenger/conversation.html', context)

def add_message(request, receiver_id):
    user_ver(request, False, True)
    
    try:
        my_message = request.POST['conversationbox']
    except:
        raise Http404("Invalid request")
    
    
    if my_message != "":
        a = Message(senderid = request.session['user_id'], receiverid = receiver_id, message = my_message)
        a.save()

    if Account.objects.get(id = request.session['user_id']).account_type == "Admin":
        return HttpResponseRedirect(reverse('adminconversation', args=(receiver_id,)))
    else:
        return HttpResponseRedirect(reverse('userconversation', args=(receiver_id,)))


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
    help_message = help_message.strip()
    
    if not help_message:
        return HttpResponseRedirect(reverse('support'))
    
    a = Message(senderid = request.session['user_id'], receiverid = receiving_admin.id, message = help_message)
    a.save()
    
    context = {}
    return HttpResponseRedirect(reverse('userconversation', args=(receiving_admin.id,)))
