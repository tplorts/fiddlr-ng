from django import template
from django.template import Context

register = template.Library()


@register.inclusion_tag('fing/about-section.html', takes_context=True)
def FingAboutSection(context):
    return context


class LalaField():
    def __init__(self, fing, name, default=''):
        self.fing = fing
        self.value = getattr(fing, name)
        self.name = name
        self.defaultValue = default

class LalaNgScope():
    def __init__(self, fingVarName):
        self.fing = fingVarName

@register.inclusion_tag('fing/field-editor.html', takes_context=True)
def FingFieldEditor(context):
    fname = context['field'].name
    c = Context({
        'ng': LalaNgScope('fing'),
    })
    c.update(context)
    return c


@register.inclusion_tag('fing/field.html', takes_context=True)
def FingField(context, fieldName, fieldTag=None):
    c = Context({
        'field': LalaField(context['fing'], fieldName),
        'fieldTag': fieldTag,
    })
    c.update(context)
    return c


