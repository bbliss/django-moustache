# Create your views here.
import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

from moustache.models import Babe

def landing(request):
    
    today = datetime.date.today()
    
    babe = Babe.objects.filter(date__day=today.day, date__month=today.month)[0]
    error_msg = rate_babe(request, babe)
    
    recent_babes = Babe.objects.filter(
        date__lt=babe.date, 
        date__gte=(babe.date - datetime.timedelta(days=3))
    )[:3]
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
        'error_msg': error_msg,
    }, context_instance = RequestContext(request))

def babe_detail(request, babe_id):
    
    babe = get_object_or_404(Babe, pk=babe_id)
    error_msg = rate_babe(request, babe)
            
    recent_babes = Babe.objects.filter(
        date__lt=babe.date, 
        date__gte=(babe.date - datetime.timedelta(days=3))
    )[:3]
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
        'error_msg': error_msg,
    }, context_instance = RequestContext(request))
    
def rate_babe(request, babe):
    
    error_msg = None
    
    if request.method == "POST":
        babes_rated = request.session.get('babes_rated', [])
        if babe.id in babes_rated:
            error_msg = 'You have already rated this babe!'
        else:
            babe_vote = request.POST.get('babevote', 0)
            if not ( int(babe_vote) in range(1, 11) ):
                babe_vote = None
                error_msg = 'Please select a vote from 1 to 10!'
            else:
                babes_rated.append(babe.id)
                request.session['babes_rated'] = babes_rated
                
                babe.rating = (babe.rating * babe.rating_count + int(babe_vote)) / (babe.rating_count + 1)
                babe.rating_count = babe.rating_count + 1
                babe.save()
                
    return error_msg
    