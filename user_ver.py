from django.http import HttpResponse, Http404
from django.template import loader
from account.models import Account

def user_ver(request, admin, both = False):
    try:
        a = request.session.get('user_id')
        b = request.session['user_id']
    except (KeyError):
        raise Http404("Unknown ID")
    else:
        if both :
            return
        if admin :
            if Account.objects.get(id=b).account_type != "Admin":
                raise Http404("Unauthorized access")
        else:
            if Account.objects.get(id=b).account_type == "Admin":
                raise Http404("Unauthorized access")

def recover_ver(request, admin, both = False):
    try:
        a = request.session.get('recover_id')
        b = request.session['recover_id']
    except (KeyError):
        raise Http404("Unknown ID")
    else:
        if both :
            return
        if admin :
            if Account.objects.get(id=b).account_type != "Admin":
                raise Http404("Unauthorized access")
        else:
            if Account.objects.get(id=b).account_type == "Admin":
                raise Http404("Unauthorized access")

