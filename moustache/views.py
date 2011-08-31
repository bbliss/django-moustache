# Create your views here.
import datetime
import calendar

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.http import Http404
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect, render


from moustache.models import Babe

def landing(request):
    
    today = datetime.date.today()
    cname = 'babe_today'
    cached_babe = cache.get(cname)
    if cached_babe:
        (babe, recent_babes) = cached_babe
    else:
        try:
            babe = Babe.objects.filter(date__day=today.day, date__month=today.month)[0]
        except IndexError:
            raise Http404
        
        recent_babes = Babe.objects.filter(
            date__lt=babe.date, 
            date__gte=(babe.date - datetime.timedelta(days=3))
        ).order_by('date')[:3]
        cache.set(cname, (babe, recent_babes), 60 * 5)
    
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
    today = datetime.datetime.today() - datetime.timedelta(days=6)                  
    acceptable_months = [today.month,
                        (today.month + 11) % 12,
                        (today.month + 10) % 12,]
    
    # Display a notice if the month requested is unavailable.
    if not int(month) in acceptable_months:
        return render(request, 'moustache/moustache_calendar.html', {
            'babe_month_unavailable': True,
        })
    
    # Figure out what the next and previous months are.
    next_month = (int(month) + 1) % 12
    prev_month = (int(month) + 11) % 12
    
    # Grab the main set of babes for the month
    calendar_babes = Babe.objects.filter(
        date__month=month,
        date__lte=today,
    ).order_by('date')
    
    upcoming_babes = Babe.objects.filter(
        date__month=month,
        date__gt=today,
    ).order_by('date')
    
    # Get the dates for the main babes
    calendar_babe_dates = calendar_babes.values_list('date')
    upcoming_babe_dates = upcoming_babes.values_list('date')

    # Figure out what the days leading into the month should be
    first_weekday = calendar_babes[0].date.weekday()
    leading_days_quantity = (first_weekday + 7) % 6
    prev_month_days = calendar.monthrange(2011, prev_month)[1]
    leading_days = []
    for i in range(0, leading_days_quantity):
        leading_days.append(datetime.date(month=prev_month, year=2011, day=prev_month_days - i))
    leading_days.reverse()
    
    # Grab the babes for the days leading into the month
    leading_babes = []
    for leading_day in leading_days:
        leading_babes.append(Babe.objects.get(date__day=leading_day.day, date__month=leading_day.month))
    
    # Figure out what the trailing days should be
    trailing_days = []
    last_day_of_month = calendar.monthrange(2011, int(month))[1]
    last_weekday_of_month = datetime.date(year=2011, month=int(month), day=last_day_of_month).weekday()
    trailing_days_quantity = 5 - last_weekday_of_month
    if trailing_days_quantity == -1:
        trailing_days_quantity = 6
    for i in range(0, trailing_days_quantity):
        trailing_days.append(datetime.date(month=next_month, year=2011, day=(i + 1)))
    
    
    day_babe_tuple_list = []
    # put all the babes and days into a list of tuples
    for i, day in enumerate(leading_days):
        day_babe_tuple_list.append({'date': day, 'babe': leading_babes[i], 'class': 'leading'})
    for i, day in enumerate(calendar_babe_dates):
        day_babe_tuple_list.append({'date': day[0], 'babe': calendar_babes[i], 'class': 'active'})
    for i, day in enumerate(upcoming_babe_dates):
        day_babe_tuple_list.append({'date': day[0], 'babe': upcoming_babes[i], 'class': 'upcoming'})
    for day in trailing_days:
        day_babe_tuple_list.append({'date': day, 'babe': None, 'class': 'blank'})
    
    weeks = []
    for i in range(0, len(day_babe_tuple_list), 7):
        weeks.append(day_babe_tuple_list[i:i+7])
        
    # Get a human readable string for the current month
    month_map = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
    month_string = month_map[int(month) - 1]
    
    return render(request, 'moustache/moustache_calendar_new.html', {
        'weeks': weeks,
        'current_month': month_string,
    })


def babe_calendar_old(request, month=datetime.datetime.today().month):
    
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
        
        
        
        
        
        todays_day = 13
        #getting number of days in the current month
        import calendar
        max_days = calendar.monthrange(datetime.date.today().year, today.month)[1]
        trailing_dates = []
        i = 1
        while i <= max_days - todays_day:
            trailing_dates.append(datetime.date(month=today.month, day=todays_day + i, year=today.year))
            i = i + 1
        
        print "trailing:", trailing_dates
    else:
        todays_day = 40
    
    return render_to_response('moustache/moustache_calendar.html', {
        'calendar_babes': calendar_babes,
        'first_weekday': calendar_babes[0].date.weekday,
        'blank_days': blank_days,
        'trailing_days': trailing_dates,
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
    
    if error_msg:
        your_rating = None
    
    return render_to_response('moustache/moustache_voting.html', {
        'new_rating': new_rating,
        'error_msg': error_msg,
        'your_rating': your_rating
    }, context_instance = RequestContext(request))
    