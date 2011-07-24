import datetime
import os
from PIL import Image

from django.conf import settings
from django.core.files import File

from moustache.models import Babe

def create_dummy_babes():
    #today = datetime.date.today()
    today = datetime.date(day=1, month=1, year=2011)
    print "today:", today
    
    for i in range(0, 365):
        p1 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p2 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p3 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p4 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p5 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        
        le_babe = Babe.objects.create(
            description='dummy babe ' + str(i),
            date = today + datetime.timedelta(days=i),
            pic1 = p1,
            pic2 = p2,
            pic3 = p3,
            pic4 = p4,
            pic5 = p5,
            rating = 5.5,
            rating_count = 3
        )
        le_babe.save()