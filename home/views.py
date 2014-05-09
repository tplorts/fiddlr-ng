from django.shortcuts import render
from fiddlr import settings


def renderView( request, template, context={} ):
    context.update({
        'isProduction': settings.isProduction,
        'useLESS': settings.TEMPLATE_DEBUG,
    })
    return render( request, template, context )




def front(q):
    return renderView(q, 'front.html')
