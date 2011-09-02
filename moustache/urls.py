from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('moustache.views',   
    url(r'^$',
        'babe_detail',
        name='moustache_babe_current',
    ),   
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'babe_detail',
        name='moustache_babe'
    ),
    
    url(r'^calendar/(?P<year>\d{4})/(?P<month>\d{2})/$',
        'babe_calendar',
        name='moustache_calendar',
    ),
    url(r'^calendar/$',
        'babe_calendar',
        name='moustache_calendar_current',
    ),
    
    url(r'^ajax/vote/$',
        'ajax_rate_babe',
        name='moustache_ajax_rate_babe',
    ),
)