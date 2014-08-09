from django import template
from django.utils.safestring import mark_safe
from django.core.serializers.json import DjangoJSONEncoder
from fiddlr import settings
import re
import pytz
import json


register = template.Library()


@register.filter
def split(string, delimiter):
    return string.split(delimiter)


@register.filter
def toJSON(something):
    return mark_safe(json.dumps(something, cls=DjangoJSONEncoder))


@register.filter
def smallcaps(text, smallSize=None):
    if smallSize:
        style = 'style="font-size: %s;"' % smallSize
    else:
        style = ''
    #TODO: how will I insert this custom style into the span?
    s = re.sub(r'([a-z]+)', r'<span class="smallcaps">\1</span>', text)
    return mark_safe(s)


@register.filter
def space2newline(text):
    o = re.sub(r'\s+', r'<br>', text)
    return mark_safe(o)


@register.inclusion_tag('tags/pallet.html')
def pallet( *args, **kwargs ):
    return kwargs


@register.inclusion_tag('tags/placeholder-copy.html')
def placeholder_copy(*args, **kwargs):
    if 'length' not in kwargs:
        kwargs['length'] = 2
    return kwargs


@register.inclusion_tag('tags/date-range.html')
def date_range( start, end ):
    start = start.astimezone(pytz.timezone(settings.TIME_ZONE))
    end = end.astimezone(pytz.timezone(settings.TIME_ZONE))
    same_month = start.month == end.month
    same_day = same_month and start.day == end.day
    return {
        'start': start,
        'end': end,
        'same_month': same_month,
        'same_day': same_day,
    }
