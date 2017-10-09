from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Account
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.conf.urls import url
from user_ver import user_ver, recover_ver
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from random import randint
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
    for ac in Account.objects.all():
        if ac.username == request.POST['name']:
            acID = ac.id
            if ac.password == request.POST['password']:
                if ac.account_type == 'Admin':
                    request.session['user_id'] = ac.id
                    return render(request, 'admin/admin_home.html', {'username': ac.username, 'ac': ac})
                request.session['user_id'] = ac.id
                return render(request, 'home/home.html', {'username': ac.username})

    return render(request, 'account/login.html', {'error_message': "Invalid information"})


def createac(request):
    context = {}
    return render(request, 'account/createac.html', context)

def createadmin(request):
    user_ver(request, True)
    context = {'admin': True}
    return render(request, 'account/createac.html', context)

def createprocess(request):
    types = ['Student', 'Tourist', 'Businessman']
    
    name = request.POST['name']
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
        if ac.username == name:
            return render(request, 'account/createac.html', {'error_message': "This username have been chosen."})
        if ac.email_address == email:
            return render(request, 'account/createac.html', {'error_message': "This email have been registered."})


    if password != confirmpw:
        return render(request, 'account/createac.html', {'error_message': "Your password does not match."})
    
    newac = Account(account_type = type, username = name, password = password, phone_number = phoneno, email_address = email, residential_address = address)
    
    newac.save()
    
    return redirect('../')


def createadminprocess(request):
    user_ver(request, True)
    
    name = request.POST['name']
    password = request.POST['password']
    confirmpw = request.POST['confirm_password']
    phoneno = request.POST['phone_number']
    email = request.POST['email']
    address = request.POST['address']
    
    for ac in Account.objects.all():
        if ac.username == name:
            return render(request, 'account/createac.html', {'error_message': "This username have been chosen.", 'admin': True})
        if ac.email_address == email:
            return render(request, 'account/createac.html', {'error_message': "This email have been registered."})

    if password != confirmpw:
        return render(request, 'account/createac.html', {'error_message': "Your password does not match.", 'admin': True})

    newac = Account(account_type = 'Admin', username = name, password = password, phone_number = phoneno, email_address = email, residential_address = address)
    
    newac.save()
    
    return redirect('../adminhome/')



def editac(request):
    user_ver(request, False)
    context = {'ac': Account.objects.get(id=request.session['user_id'])}
    return render(request, 'account/edit_account_details.html', context)

def editacsave(request):
    user_ver(request, False)
    all_ac = Account.objects.all()
    user_ac = Account.objects.get(id=request.session['user_id'])
    
    acname = request.POST['Username']
    acemail = request.POST['emailaddress']
    error = "Edit successful"
    
    for ac in all_ac:
        if acname != user_ac.username and ac.username == acname:
            error = "This username have been chosen."
        if acemail != user_ac.email_address and ac.email_address == acemail:
            error = "This email have been registered."

    old_pw = request.POST['old_password']
    new_pw = request.POST['new_password']
    confirm_pw = request.POST['confirm_password']

    if (old_pw):
        if (user_ac.password == old_pw and new_pw == confirm_pw):
            user_ac.password = new_pw
        else:
            error = "Invalid password"

    if error == "Edit successful":
        user_ac.username = acname
        user_ac.email_address = acemail
        user_ac.residential_address = request.POST['address']
        user_ac.phone_number = request.POST['contactnumber']
        user_ac.save()
    
    context = {'ac': user_ac, 'message': error}
    return render(request, 'account/edit_account_details.html', context)

def recoverac(request):
    return render(request, 'account/recover_account.html')

def recoverusername(request):
    try:
        ac = Account.objects.filter(email_address = request.POST['email'])
    except MultiValueDictKeyError:
        raise Http404("Unknown ID")

    if (not ac):
        return render(request, 'account/recover_account.html', {'warning': "This email does not exist"})
    request.session['recover_id'] = ac[0].id
    context = {'username': ac[0].username}
    return render(request, 'account/recover_username.html', context)

def recoverpassword(request):
    recover_ver(request, False, True)
    ac = Account.objects.get(id = request.session['recover_id'])
    #secretcode = ""
    #secretcode = (str)randint(0, 9)
    #for each in range(5):
    #    secretcode += (str)randint(0, 9)
    secretcode = "123456"
    request.session['secretcode'] = secretcode
    #send_mail('Account Recovery Email for Smart City', 'Hello, ' + ac.username + '\nHere is your secret code: ' + secretcode, 'sc@smartcity.com', [ac.email_address], fail_silently=False,)
    context = {}
    return render(request, 'account/recover_password.html', context)

def recoverpasswordconfirm(request):
    recover_ver(request, False, True)
    
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
    return redirect('../')




