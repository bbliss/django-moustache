import datetime
import os
from PIL import Image

from moustache.models import Babe

def create_dummy_babes():
    today = datetime.date.today()
    dummy_image = 

    for i in range(1, 365):
        Babe.objects.create(
            description='dummy babe ' + str(i),
            date = datetime.date.today + datetime.timedelta(days=1),
            pic1 = Image.open(settings.MEDIA_ROOT + 'moustache/babe1.jpg')