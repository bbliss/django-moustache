# Create your views here.
import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

from moustache.models import Babe

def moustache_landing(request):
    
    babe = Babe.objects.all()[0]
    
    if request.method == "POST":
        babes_rated = request.session.get('babes_rated', None)
        if babes_rated:
            error_msg = 'You have already rated this babe!'
            print error_msg
        else:
            request.session['babes_rated'] = babe.id
            
            #print "post data:", request.POST['babevote']
            babe_vote = request.POST['babevote']
            #if not ( int(babe_vote) in range(1, 10) ):
            #    babe_vote = None
            #    print "unexpected form data"
            #else:
            babe.rating = (babe.rating * babe.rating_count + int(babe_vote)) / (babe.rating_count + 1)
            print "new babe rating:", babe.rating
            babe.save()
            
    babe_list = []
    for i in range(1, 35):
        babe_list.append(i)
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'babe_calendar_list': babe_list,
    }, context_instance = RequestContext(request))
    
def moustache_vote(request):
    
    babe = Babe.objects.all()[0]
    
    if request.method == "POST":
        babes_rated = request.session.get('babes_rated', None)
        if babes_rated:
            error_msg = 'You have already rated this babe!'
            print error_msg
        else:
            request.session['babes_rated'] = babe.id
            
            #print "post data:", request.POST['babevote']
            babe_vote = request.POST['babevote']
            #if not ( int(babe_vote) in range(1, 10) ):
            #    babe_vote = None
            #    print "unexpected form data"
            #else:
            babe.rating = (babe.rating * babe.rating_count + int(babe_vote)) / (babe.rating_count + 1)
            print "new babe rating:", babe.rating
            babe.save()
        
    
    return render_to_response('moustache/moustache_vote.html', {
        'babe': babe,
    }, context_instance = RequestContext(request))