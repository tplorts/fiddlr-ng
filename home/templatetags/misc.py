from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.filter
def split(string, delimiter):
    return string.split(delimiter)



class DefaultJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

@register.filter
def tojson(obj):
    return mark_safe( json.dumps(obj, cls=DefaultJSONEncoder, separators=(',', ':')) )
