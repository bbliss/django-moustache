from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('moustache.views',
    
    url(r'^$',
        'moustache_landing',
        name='moustache_landing'
    ),
    url(r'^vote/$',
        'moustache_vote',
        name='moustache_vote'
    ),
)