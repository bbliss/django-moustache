import datetime
import os
from PIL import Image

from django.conf import settings
from django.core.files import File

from moustache.models import Babe

def create_dummy_babes():
    today = datetime.date(day=1, month=1, year=2011)
    print "today:", today
    
    for i in range(0, 365):
        p1 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p2 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p3 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p4 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p5 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        p6 = File(open(settings.MEDIA_ROOT + 'moustache/babe1.jpg', 'rb'))
        
        le_babe = Babe.objects.create(
            name='dummy babe ' + str(i),
            date = today + datetime.timedelta(days=i),
            pic1 = p1,
            pic2 = p2,
            pic3 = p3,
            pic4 = p4,
            pic5 = p5,
            pic6 = p6,
            rating = 5.5,
            rating_count = 3
        )
        le_babe.save()
        
def make_babes():
    
    first_day = datetime.date(day=1, month=6, year=2011)
    i = 0
    
    babe_root_folder = settings.MEDIA_ROOT + "raw_babes"
    babe_folders = os.listdir(babe_root_folder)
    for folder in babe_folders:
        if folder == '.DS_Store':
            print "DERP DS STORE FOUND"
            continue
        
        babe_name = folder
        #print "babe name:", babe_name
        
        pic_files = []
        for babe_pic in os.listdir(babe_root_folder + '/' + babe_name):
            #print "pic:", babe_pic
            if not (babe_pic.endswith('.jpg') or babe_pic.endswith('.JPG') or babe_pic.endswith('.Jpg')):
                print "non jpg image found:", babe_pic
                continue
            pic_files.append(File(open(babe_root_folder + '/' + babe_name + '/' + babe_pic)))
            
        le_babe = Babe.objects.create(
            name = babe_name,
            date = first_day + datetime.timedelta(days=i),
            pic1 = pic_files[0],
            pic2 = pic_files[1],
            pic3 = pic_files[2],
            rating = 5,
            rating_count = 1,
        )
        try:
            le_babe.pic4 = pic_files[4]
        except IndexError:
            pass
        try:
            le_babe.pic5 = pic_files[5]
        except IndexError:
            pass
        try:
            le_babe.pic6 = pic_files[6]
        except IndexError:
            pass
        
        le_babe.save()
        print "babe added:", i
        i = i + 1
            
