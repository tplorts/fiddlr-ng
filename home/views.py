from django.shortcuts import render
from fiddlr import settings


def renderView( request, template, context={} ):
    context.update({
        'isProduction': settings.isProduction,
        'useLESS': settings.TEMPLATE_DEBUG,
    })
    return render( request, template, context )

def renderPage( request, pageName, context={} ):
    context.update({
        'pageName': pageName.capitalize(),
    })
    return renderView( request, pageName+'.html', context )


def front(q):
    return renderPage(q, 'front')


def explore(q):
    initial_markers = (
        {'latitude': 40.7363114,
         'longitude': -73.9908941},
        {'latitude': 40.765936,
         'longitude': -73.984026},
    )
    return renderPage(q, 'explore', {
        'gmaps_api_key': settings.gmaps_api_key,
        'initial_markers': initial_markers,
    })

def create(q):
    return renderPage(q, 'create')

def connect(q):
    return renderPage(q, 'connect')



def about(q):
    return renderPage(q, 'about')

def copyrightView(q):
    return renderPage(q, 'copyright')

def helpView(q):
    return renderPage(q, 'help')

def adsView(q):
    return renderPage(q, 'ads')

