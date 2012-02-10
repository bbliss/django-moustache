# Create your views here.
import datetime
import calendar

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.utils import timezone

from moustache.models import Babe

def babe_detail(request, year=None, month=None, day=None):
    
    try:
        babe_date = datetime.date(year=int(year), month=int(month), day=int(day))
    except TypeError:
        babe_date = timezone.now().date()
    
    today = timezone.now().date()
    first_of_todays_month = datetime.date(day=1, month=today.month, year=today.year)
    max_date = today
    min_date = first_of_todays_month - datetime.timedelta(days=68)
    if babe_date < min_date or babe_date > max_date:
        return render(request, 'moustache/moustache_landing.html', {
            'babe_unavailable': True,
        })
            
    cname = 'babe_detail_' + str(babe_date)
    cached_babe = cache.get(cname)
    if cached_babe:
        (babe, recent_babes) = cached_babe
    else:
        babe = get_object_or_404(Babe, date=babe_date)       
        recent_babes = Babe.objects.filter(
            date__lt=babe_date, 
            date__gte=(babe_date - datetime.timedelta(days=3))
        ).order_by('date')[:3]
        cache.set(cname, (babe, recent_babes), 60 * 30)
    
    return render_to_response('moustache/moustache_landing.html', {
        'babe': babe,
        'recent_babes': recent_babes,
    }, context_instance = RequestContext(request))

def babe_calendar(request, year=None, month=None):
    
    # Calculate the first and last days of the month, rendering an unavailable
    # message if babes older than 60 days would be shown.
    today = timezone.now().date()
    first_of_todays_month = datetime.date(day=1, month=today.month, year=today.year)
    try:
        first_of_month = datetime.date(year=int(year), month=int(month), day=1)
        last_of_month = datetime.date(year=int(year), month=int(month), 
            day=calendar.monthrange(int(year), int(month))[1])
        
        
        if first_of_month > today or last_of_month < (first_of_todays_month - datetime.timedelta(days=62)):            
            return render(request, 'moustache/moustache_calendar_new.html', {
                'babe_month_unavailable': True,
            })          
    except TypeError:
        first_of_month = datetime.date(year=today.year, month=today.month, day=1)
        last_of_month = datetime.date(year=today.year, month=today.month, 
            day=calendar.monthrange(today.year, today.month)[1])
    
    # Get a human readable string for the current month
    month_map = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
    month_string = month_map[first_of_month.month - 1]
    
    # Calculate next and previous months, and if they're available
    prev_month = first_of_month - datetime.timedelta(days=1)
    next_month = last_of_month + datetime.timedelta(days=1)
    if first_of_month - datetime.timedelta(days=1) < (today - datetime.timedelta(days=62)):
        prev_month = None
    else:
        prev_month = (prev_month.year, str(prev_month.month).zfill(2))
    if last_of_month + datetime.timedelta(days=1) > today:
        next_month = None
    else:
        next_month = (next_month.year, str(next_month.month).zfill(2))
    
    # Check if the requested month's babes are cached, if so, we can skip
    # doing any quering to fetch them and render the template
    cname = 'babe_calendar_' + str(first_of_month)
    cached_weeks = cache.get(cname)
    if cached_weeks:
        return render(request, 'moustache/moustache_calendar_new.html', {
            'weeks': cached_weeks,
            'current_month': month_string,
            'next_month': next_month,
            'prev_month': prev_month,
        })
    
    # Grab active and upcoming babes for the month
    if today >= first_of_month and today <= last_of_month:
        active_babes = Babe.objects.filter(
            date__lte=today,
            date__gte=first_of_month
        ).order_by('date')
        upcoming_babes = Babe.objects.filter(
            date__gt=today,
            date__lte=last_of_month
        ).order_by('date')
    else:
        active_babes = Babe.objects.filter(
            date__lte=last_of_month,
            date__gte=first_of_month
        ).order_by('date')
        upcoming_babes = []
    
    #Create a list of trailing dates to complete the calendar row
    trailing_days = []
    trailing_days_quantity = 5 - last_of_month.weekday()
    if trailing_days_quantity == -1:
        trailing_days_quantity = 6
    for i in range(0, trailing_days_quantity):
        trailing_days.append(datetime.date(
            month=(last_of_month + datetime.timedelta(days=1)).month, 
            year=(last_of_month + datetime.timedelta(days=1)).year, day=(i + 1)))

    #Grab the last few babes from the previous month to complete the calendar row
    leading_days_quantity = (first_of_month.weekday() + 1) % 7
    leading_babes = list(Babe.objects.filter(date__lt=first_of_month).order_by('-date')[:leading_days_quantity])
    leading_babes.reverse()
    
    # Put all the babes and days into a list of dictionaries
    day_dict_list = []
    for babe in leading_babes:
        day_dict_list.append({'date': babe.date, 'babe': babe, 'class': 'leading'})
    for babe in active_babes:
        day_dict_list.append({'date': babe.date, 'babe': babe, 'class': 'active'})
    for babe in upcoming_babes:
        day_dict_list.append({'date': babe.date, 'babe': babe, 'class': 'upcoming'})
    for day in trailing_days:
        day_dict_list.append({'date': day, 'babe': None, 'class': 'blank'})
    
    # Split the list of dictionaries into lists for each week so that they're
    # Easy to display in <tr> on the template.
    weeks = []
    for i in range(0, len(day_dict_list), 7):
        weeks.append(day_dict_list[i:i+7])
    cache.set(cname, weeks, 60 * 30)

    return render(request, 'moustache/moustache_calendar_new.html', {
        'prev_month': prev_month,
        'next_month': next_month,
        'weeks': weeks,
        'current_month': month_string,
    })

def ajax_rate_babe(request):
    
    if not request.is_ajax:
        raise Http404
     
    babe_id = request.POST.get('babe', None)  
    babe = get_object_or_404(Babe, pk=babe_id)
    another_babe = Babe.objects.get(date=(babe.date - datetime.timedelta(days=1)))
        
    if request.method == "POST":
        babes_rated = request.session.get('babes_rated', [])
        vote = request.POST.get('babe-rating', 0)
        
        if not ( int(vote) in range(1, 11) ):
            error_msg = 'Please select a vote from 1 to 10!'
            vote = None
        if babe.id in babes_rated:
            error_msg = 'You have already rated this babe!'
            vote = None
        
        if vote:
            babes_rated.append(babe.id)
            request.session['babes_rated'] = babes_rated
            
            babe.rating = (babe.rating * babe.rating_count + int(vote)) / (babe.rating_count + 1)
            babe.rating_count = babe.rating_count + 1
            babe.save()
            error_msg = None
                        
        return render_to_response('moustache/moustache_voting.html', {
            'new_rating': babe.rating,
            'error_msg': error_msg,
            'your_rating': vote,
            'another_babe': another_babe
        }, context_instance = RequestContext(request))
    
    raise Http404
