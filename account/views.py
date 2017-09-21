from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Account
from django.template import loader
from django.utils.datastructures import MultiValueDictKeyError
from django.conf.urls import url
#from Smartcity import urls


def user_ver(request):
    try:
        request.session[user_id]
    except KeyError:
        return Http404("Unknown user")

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
                    return render(request, 'admin/admin_home.html', {'username': ac.username})
                request.session['user_id'] = ac.id
                return render(request, 'home/home.html', {'username': ac.username})

    return render(request, 'account/login.html', {'error_message': "Invalid information"})


def createac(request):
    context = {}
    return render(request, 'account/createac.html', context)

def createadmin(request):
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

    newac = Account(account_type = 'admin', username = name, password = password, phone_number = phoneno, email_address = email, residential_address = address)
    
    newac.save()
    
    return redirect('../adminhome/')



def editac(request):
    user_ver(request)
    context = {'ac': Account.objects.get(id=request.session['user_id'])}
    return render(request, 'account/edit_account_details.html', context)

def editacsave(request):
    user_ver(request)
    
    
    context = {'ac': Account.objects.get(id=request.session['user_id']), 'message': "Edit successful"}
    return render(request, 'account/edit_account_details.html', context)

def logout(request):
    user_ver(request)
    del request.session['user_id']
    return redirect('../')




