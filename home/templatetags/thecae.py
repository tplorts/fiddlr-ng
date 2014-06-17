from django import template

register = template.Library()


@register.inclusion_tag('thecae/artist.html')
def artist_theca( artist ):
    return {'artist': artist}


@register.inclusion_tag('thecae/venue.html')
def venue_theca( venue ):
    return {'venue': venue}


@register.inclusion_tag('thecae/event.html')
def event_theca( event ):
    return {'event': event}

