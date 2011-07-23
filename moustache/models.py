from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Babe(models.Model):
    description = models.CharField(max_length=200)
    date = models.DateField()
    
    pic1 = models.ImageField(upload_to='moustache/')
    pic2 = models.ImageField(upload_to='moustache/')
    pic3 = models.ImageField(upload_to='moustache/')
    pic4 = models.ImageField(upload_to='moustache/')
    pic5 = models.ImageField(upload_to='moustache/')
    
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    rating_count = models.IntegerField()
    
    def __unicode__(self):
        if self.description:
            return 'Babe for ' + str(self.date) + ' (' + self.description + ')'
        else:
            return 'Babe for ' + str(self.date)
            
    def get_absolute_url(self):
        return reverse('moustache_babe_detail', args=[self.id])