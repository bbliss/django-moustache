# Create your views here.
import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect

from moustache.models import Babe

def landing(request):
    
    today = datetime.date.today()
    babe = Babe.objects.filter(date__day=today.day, date__month=today.month)[0]
    
    if not babe:
        raise Http404
    
    recent_babes = Babe.objects.filter(
        date__lt=babe.date, 
        date__gte=(babe.date - datetime.timedelta(days=3))
    ).order_by('date')[:3]
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
    }, context_instance = RequestContext(request))

def babe_detail(request, babe_id):
    
    babe = get_object_or_404(Babe, pk=babe_id)
            
    recent_babes = Babe.objects.filter(
        date__lt=babe.date, 
        date__gte=(babe.date - datetime.timedelta(days=3))
    ).order_by('date')[:3]
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
    }, context_instance = RequestContext(request))
   
def babe_calendar(request, month=datetime.datetime.today().month):
    
    calendar_babes = Babe.objects.filter(
        date__month=month,
    ).order_by('date')
    
    if not calendar_babes:
        raise Http404
    
    first_weekday = calendar_babes[0].date.weekday()
    print "first weekday:", first_weekday
    blank_days = []
    for i in range(0, int(first_weekday)):
        blank_days.append('day')
        print "adding for i:", i
    
    return render_to_response('moustache/moustache_calendar.html', {
        'calendar_babes': calendar_babes,
        'first_weekday': calendar_babes[0].date.weekday,
        'blank_days': blank_days,
    }, context_instance = RequestContext(request))
    
def ajax_rate_babe(request):
    
    if not request.is_ajax:
        raise Http404
     
    babe_id = request.POST.get('babe', None)
    babe_rating = request.POST.get('babe-rating', None)
        
    babe = get_object_or_404(Babe, pk=babe_id) #Babe.objects.filter(pk=babe_id)[0]
    
    error_msg = "You rated this babe a " + str(babe_rating) + "!"
    new_rating = babe.rating
    
    if request.method == "POST":
        babes_rated = request.session.get('babes_rated', [])
        if babe.id in babes_rated:
            error_msg = 'You have already rated this babe!'
        else:
            babe_vote = request.POST.get('babe-rating', 0)
            if not ( int(babe_vote) in range(1, 11) ):
                babe_vote = None
                error_msg = 'Please select a vote from 1 to 10!'
            else:
                babes_rated.append(babe.id)
                request.session['babes_rated'] = babes_rated
                
                babe.rating = (babe.rating * babe.rating_count + int(babe_vote)) / (babe.rating_count + 1)
                babe.rating_count = babe.rating_count + 1
                new_rating = babe.rating
                babe.save()
    
    return render_to_response('moustache/moustache_voting.html', {
        'new_rating': new_rating,
        'error_msg': error_msg,
    }, context_instance = RequestContext(request))
    