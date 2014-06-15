from django import template

register = template.Library()


@register.inclusion_tag('thecae/artist.html')
def artist_theca( artist ):
    return {'artist': artist}

