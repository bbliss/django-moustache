# Create your views here.
import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect, render


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
    
    cname = 'babe_detail_' + str(babe_id)
    cached_babe = cache.get(cname)
    if cached_babe:
        (babe, recent_babes) = cached_babe
    else:
        babe = get_object_or_404(Babe, pk=babe_id)
                
        recent_babes = Babe.objects.filter(
            date__lt=babe.date, 
            date__gte=(babe.date - datetime.timedelta(days=3))
        ).order_by('date')[:3]
        cache.set(cname, (babe, recent_babes), 60 * 30)
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
    }, context_instance = RequestContext(request))
   
def babe_calendar(request, month=datetime.datetime.today().month):
    
    # Figure out what months should be viewable, for now this is the current
    # month and the 3 previous months.
    today = datetime.datetime.today()                  
    acceptable_months = [today.month,
                        (today.month + 11) % 12,
                        (today.month + 10) % 12,]
                        #(today.month + 9) % 12,]
    
    # Display a notice if the month requested is unavailable.
    if not int(month) in acceptable_months:
        return render(request, 'moustache/moustache_calendar.html', {
            'babe_month_unavailable': True,
        })
    
    cname = 'babe_calendar_' + str(month)
    cached_babes = cache.get(cname)
    if cached_babes:
        calendar_babes = cached_babes
    else:
        # Fetch the babes from the database.
        calendar_babes = Babe.objects.filter(
            date__month=month,
            #date__day=today.day,
        ).order_by('date')
        if not calendar_babes:
            raise Http404
        else:
            cache.set(cname, calendar_babes, 60 * 30)
    
    # Figure out if we need to pad the calendar with blank days.
    first_weekday = calendar_babes[0].date.weekday()
    blank_days = []
    for i in range(0, int(first_weekday) + 1):
        if int(first_weekday) == 6:
            break
        blank_days.append('day')
    
    # Figure out what the next and previous months are.
    next_month = (int(month) + 1) % 12
    prev_month = (int(month) + 11) % 12
    
    # Determine what the links to previous and next months should be, if those
    # months are within the available range.
    next_month_id = prev_month_id = None
    if next_month in acceptable_months:
        next_month_id = next_month        
    if prev_month in acceptable_months:
        prev_month_id = prev_month
    
    # Grab the string for the requested month's name.
    month_map = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
    month_string = month_map[int(month) - 1]
    
    # If the month being viewed is not the current month, show all days.
    print "month:", month
    print "today.month:", today.month
    if int(month) == today.month:
        todays_day = today.day
        print "setting day to", todays_day
    else:
        todays_day = 40
    
    return render_to_response('moustache/moustache_calendar.html', {
        'calendar_babes': calendar_babes,
        'first_weekday': calendar_babes[0].date.weekday,
        'blank_days': blank_days,
        'month_string': month_string,
        'prev_month': prev_month_id,
        'next_month': next_month_id,
        'todays_day': todays_day,
        'babe_month_unavailable': False,
    }, context_instance = RequestContext(request))
    
def ajax_rate_babe(request):
    
    if not request.is_ajax:
        raise Http404
     
    babe_id = request.POST.get('babe', None)
    babe_rating = request.POST.get('babe-rating', None)
    your_rating = babe_rating
    
    babe = get_object_or_404(Babe, pk=babe_id) #Babe.objects.filter(pk=babe_id)[0]
    
    error_msg = None
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
        'your_rating': your_rating
    }, context_instance = RequestContext(request))
    