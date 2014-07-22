from django import template
from django.template import Context

register = template.Library()


@register.inclusion_tag('creo/about-section.html', takes_context=True)
def CreoAboutSection(context):
    return context



@register.inclusion_tag('creo/field.html', takes_context=True)
def CreoField(context, fieldName):
    c = Context({
        'fieldName': fieldName,
        'fieldTag': context['creoForm'][fieldName],
    })
    c.update(context)
    return c



@register.inclusion_tag('creo/image-field.html', takes_context=True)
def CreoImageField(context, fieldName):
    lp = 'http://lorempixel.com/350/450/animals'
    return CreoField(context, fieldName)



@register.inclusion_tag('creo/location-field.html', takes_context=True)
def CreoLocationField(context):
    return CreoField(context, 'location')
