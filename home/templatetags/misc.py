from django import template
from django.utils.safestring import mark_safe
from fiddlr import settings
import re
import pytz


register = template.Library()


@register.filter
def split(string, delimiter):
    return string.split(delimiter)




@register.filter
def smallcaps(text):
    o = re.sub(r'([a-z]+)', r'<span class="smallcaps">\1</span>', text)
    return mark_safe(o)


@register.filter
def space2newline(text):
    o = re.sub(r'\s+', r'<br>', text)
    return mark_safe(o)


@register.inclusion_tag('pallet.html')
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


@register.inclusion_tag('tags/thing-info.html')
def thingInfo(thing):
    return {
        'thing': thing,
    }
