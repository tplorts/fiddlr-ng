from django import template
register = template.Library()

@register.filter
def split(string, delimiter):
    return string.split(delimiter)

