from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Account
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.conf.urls import url
from user_ver import user_ver
from django.urls import reverse
from django.http import HttpResponseRedirect
#return HttpResponseRedirect(reverse('adminconversation', args=(receiver_id,)))

# Create your views here.             ACCOUNT VIEW

def login(request):
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
    user_ac = Account.objects.get(id=request.session['user_id'])
    
    user_ac.username = request.POST['Username']
    user_ac.residential_address = request.POST['address']
    user_ac.phone_number = request.POST['contactnumber']
    user_ac.email_address = request.POST['emailaddress']
    
    old_pw = request.POST['old_password']
    new_pw = request.POST['new_password']
    confirm_pw = request.POST['confirm_password']
    
    error = "Edit successful"
    if (user_ac.password == old_pw and new_pw == confirm_pw):
        user_ac.password = new_pw
    else:
        error = "Invalid password"
    
    user_ac.save()
    
    context = {'ac': user_ac, 'message': error}
    return render(request, 'account/edit_account_details.html', context)

def logout(request):
    user_ver(request, False, True)
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect('../')




