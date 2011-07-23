# Create your views here.
import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

from moustache.models import Babe

def moustache_landing(request):
    
    herf = 'derf'
    babe = Babe.objects.all()[0]
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
    }, context_instance = RequestContext(request)) 