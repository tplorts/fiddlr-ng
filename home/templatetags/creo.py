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
    })
    if context['isEditing']:
        c.update({
            'fieldTag': context['creoForm'][fieldName],
        })
    c.update(context)
    return c



@register.inclusion_tag('creo/image-field.html', takes_context=True)
def CreoImageField(context, fieldName):
    return CreoField(context, fieldName)


@register.inclusion_tag('creo/formatted-text-field.html', takes_context=True)
def CreoFormattedTextField(context, fieldName):
    return CreoField(context, fieldName)


@register.inclusion_tag('creo/location-field.html', takes_context=True)
def CreoLocationField(context):
    return CreoField(context, 'location')
