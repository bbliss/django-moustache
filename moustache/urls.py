from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('moustache.views',
    
    url(r'^$',
        'landing',
        name='moustache_landing'
    ),

    url(r'^babe/(?P<babe_id>\d+)/$',
        'babe_detail',
        name='moustache_babe_detail',
    ),
    
    url(r'^calendar/$',
        'babe_calendar',
        name='moustache_babe_calendar_current',
    ),
    url(r'^calendar/(?P<month>\d+)/$',
        'babe_calendar',
        name='moustache_babe_calendar',
    ),
    
    url(r'^oldcalendar/(?P<month>\d+)/$',
        'babe_calendar_old',
        name='moustache_babe_calendar_old',
    ),
    
    url(r'^ajax/vote/$',
        'ajax_rate_babe',
        name='moustache_ajax_rate_babe',
    ),
)