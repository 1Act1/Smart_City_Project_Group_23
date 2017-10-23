from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Account
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.conf.urls import url
from user_ver import user_ver, recover_ver, process_access
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from random import randint
from math import log
#return HttpResponseRedirect(reverse('adminconversation', args=(receiver_id,)))

# Create your views here.             ACCOUNT VIEW

def login(request):
    try:
        del request.session['recover_id']
    except KeyError:
        pass
    try:
        del request.session['secretcode']
    except KeyError:
        pass
    try:
        del request.session['user_id']
    except KeyError:
        pass
    context = {} #parameters passing to the html: {'accounts' = all_accounts}
    return render(request, 'account/login.html', context)

def loginver(request):
    process_access(request, 'name')
    
    for ac in Account.objects.all():
        if ac.username == request.POST['name']:
            acID = ac.id
            if ac.password == request.POST['password']:
                if ac.account_type == 'Admin':
                    request.session['user_id'] = ac.id
                    return HttpResponseRedirect(reverse('adminhome'))
                request.session['user_id'] = ac.id
                return HttpResponseRedirect(reverse('userhome'))

    return render(request, 'account/login.html', {'error_message': "Invalid information"})


def createac(request):
    context = {}
    return render(request, 'account/createac.html', context)

def createadmin(request):
    user_ver(request, True)
    context = {'admin': True}
    return render(request, 'account/createac.html', context)

def createprocess(request):
    process_access(request, 'yourname')
    
    types = ['Student', 'Tourist', 'Businessman']
    
    yourname = request.POST['yourname']
    user_name = request.POST['username']
    password = request.POST['password']
    confirmpw = request.POST['confirm_password']
    phoneno = request.POST['phone_number']
    email = request.POST['email']
    address = request.POST['address']
    try:
        typeno = request.POST['actype']
    except MultiValueDictKeyError:
        return render(request, 'account/createac.html', {'error_message': "Please choose your account type."})
    else:
        type = types[int(typeno) - 1]
    
    for ac in Account.objects.all():
        if ac.username == user_name:
            return render(request, 'account/createac.html', {'error_message': "This username have been chosen."})
        if ac.email_address == email:
            return render(request, 'account/createac.html', {'error_message': "This email have been registered."})


    if password != confirmpw:
        return render(request, 'account/createac.html', {'error_message': "Your password does not match."})
    
    newac = Account(name = yourname, account_type = type, username = user_name, password = password, phone_number = phoneno, email_address = email, residential_address = address)
    
    newac.save()

    subject = 'Welcome to Smart City!'
    from_email = settings.DEFAULT_FROM_EMAIL
    message = ''
    recipient_list = [newac.email_address]
    html_message = '<h3>' + 'Hello, ' + newac.username + '<br><br>Here is a warm welcome from SmartCity, feel free to browse the website and enjoy your time! ' + '<br><br>Smart City</h3>'

    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)

    return HttpResponseRedirect(reverse('login'))


def createadminprocess(request):
    user_ver(request, True)
    process_access(request, 'yourname')
    
    yourname = request.POST['yourname']
    username = request.POST['username']
    password = request.POST['password']
    confirmpw = request.POST['confirm_password']
    phoneno = request.POST['phone_number']
    email = request.POST['email']
    address = request.POST['address']
    
    for ac in Account.objects.all():
        if ac.username == username:
            return render(request, 'account/createac.html', {'error_message': "This username have been chosen.", 'admin': True})
        if ac.email_address == email:
            return render(request, 'account/createac.html', {'error_message': "This email have been registered."})

    if password != confirmpw:
        return render(request, 'account/createac.html', {'error_message': "Your password does not match.", 'admin': True})

    newac = Account(name = yourname, account_type = 'Admin', username = username, password = password, phone_number = phoneno, email_address = email, residential_address = address)
    
    newac.save()

    return HttpResponseRedirect(reverse('adminhome'))



def editac(request):
    user_ver(request, False)
    context = {'ac': Account.objects.get(id=request.session['user_id'])}
    return render(request, 'account/edit_account_details.html', context)

def editacsave(request):
    user_ver(request, False)
    process_access(request, 'yourname')
    
    all_ac = Account.objects.all()
    user_ac = Account.objects.get(id=request.session['user_id'])
    
    acname = request.POST['yourname']
    acusername = request.POST['Username']
    acemail = request.POST['emailaddress']
    error = "Edit successful"
    
    for ac in all_ac:
        if acusername != user_ac.username and ac.username == acusername:
            error = "This username have been chosen."
        if acemail != user_ac.email_address and ac.email_address == acemail:
            error = "This email have been registered."

    old_pw = request.POST['old_password']
    new_pw = request.POST['new_password']
    confirm_pw = request.POST['confirm_password']

    if (new_pw or old_pw or confirm_pw):
        if (user_ac.password == old_pw and new_pw == confirm_pw):
            user_ac.password = new_pw
        else:
            error = "Invalid password"

    if error == "Edit successful":
        user_ac.name = acname
        user_ac.username = acusername
        user_ac.email_address = acemail
        user_ac.residential_address = request.POST['address']
        user_ac.phone_number = request.POST['contactnumber']
        user_ac.save()
    
    context = {'ac': user_ac, 'message': error}
    return render(request, 'account/edit_account_details.html', context)

def recoverac(request):
    return render(request, 'account/recover_account.html')

def recoverusername(request):
    
    process_access(request, 'email')

    ac = Account.objects.filter(email_address = request.POST['email'])

    if (not ac):
        return render(request, 'account/recover_account.html', {'warning': "This email does not exist"})
    request.session['recover_id'] = ac[0].id
    context = {'username': ac[0].username}
    return render(request, 'account/recover_username.html', context)

def recoverpassword(request):
    recover_ver(request, False, True)
    
    ac = Account.objects.get(id = request.session['recover_id'])
    
    rand = randint(0, 999999)
    secretcode = ''
    for each in range(5 - (int)(log(rand, 10))):
        secretcode += '0'
    secretcode += str(rand)
    #secretcode = "123456"
    request.session['secretcode'] = secretcode

    subject = 'Account Recovery Email from Smart City'
    from_email = settings.DEFAULT_FROM_EMAIL
    message = ''
    recipient_list = [ac.email_address]
    html_message = '<h3>' + 'Hello, ' + ac.username + '<br><br>Here is your secret code: ' + secretcode + '<br><br>Smart City</h3>'


    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
    
    context = {}
    return render(request, 'account/recover_password.html', context)

def recoverpasswordconfirm(request):
    recover_ver(request, False, True)
    process_access(request, 'secretcode')
    
    actualcode = request.session['secretcode']
    secretcode = request.POST['secretcode']
    if actualcode != secretcode:
        context = {'error_message': 'Incorrect code! Recovery failed'}
        return render(request, 'account/login.html', context)
    
    new_password = request.POST['password']
    confirm_password = request.POST['confirmpassword']
    if new_password != confirm_password:
        context = {'error_message': 'Different password given! Recovery failed'}
        return render(request, 'account/login.html', context)

    ac = Account.objects.get(id = request.session['recover_id'])
    ac.password = new_password
    ac.save()

    #logout of recover_id
    try:
        del request.session['recover_id']
    except KeyError:
        pass
    try:
        del request.session['secretcode']
    except KeyError:
        pass
    context = {'error_message': 'Password saved'}
    return render(request, 'account/login.html', context)


def logout(request):
    user_ver(request, False, True)
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('login'))




