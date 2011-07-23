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
)