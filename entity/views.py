from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Entity
from django.template import loader
from user_ver import user_ver

# Create your views here.             ENTITY VIEW

def list(request):
    user_ver(request, False)
    context = {'entity_list': Entity.objects.all() }
    return render(request, 'entity/list.html', context)

def detail(request, entity_id):
    user_ver(request, False)
    context = {'entity': get_object_or_404(Entity, id = entity_id)}
    return render(request, 'entity/detail.html', context)

#ADMIN

def admin_entity_list(request):
    user_ver(request, True)
    context = {}
    return render(request, 'admin/admin_home.html', context)



#def review(request, entity_id):
#   entity = Entity.objects.get(id = entity_id)
#   selected = request.POST['review']
#
#
#   if (selected == '1' or selected == '0'):
#       if(selected == '1'):
#           entity.positive_review += 1
#       else:
#           entity.negative_review += 1
#       entity.save()
#
#   context = {'entity': get_object_or_404(Entity, id = entity_id)}
#
#
#   return render(request, 'entity/detail.html', context)
