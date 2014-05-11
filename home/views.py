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


def explore(q):
    return renderView(q, 'explore.html')

def create(q):
    return renderView(q, 'create.html')

def connect(q):
    return renderView(q, 'connect.html')



def about(q):
    return renderView(q, 'about.html')

def copyrightView(q):
    return renderView(q, 'copyright.html')

def helpView(q):
    return renderView(q, 'help.html')

