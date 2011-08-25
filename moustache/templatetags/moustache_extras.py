import datetime
from django import template

from moustache.models import Babe

register = template.Library()

class GetBabe(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name
        
    def render(self, context):
        
        try:
            today = datetime.date.today()
            babe = Babe.objects.filter(date__day=today.day, date__month=today.month)
            context[self.var_name] = babe[0]    
        except:
            context[self.var_name] = None
        
        return ''
        
@register.tag
def get_todays_babe(parser, token):
    """
    Get the image for the current babe of the day
    
    Syntax:
    {% get_babe_image as [var_name] %}
    """
    
    args = token.split_contents()
    var_name = args[-1]
    return GetBabe(var_name)