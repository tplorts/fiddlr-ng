from django import template
from django.template import Context

register = template.Library()


@register.inclusion_tag('creo/about-section.html', takes_context=True)
def CreoAboutSection(context):
    return context


class LalaField():
    def __init__(self, creo, name, default=''):
        self.creo = creo
        self.value = getattr(creo, name)
        self.name = name
        self.defaultValue = default

class LalaNgScope():
    def __init__(self, creoVarName):
        self.creo = creoVarName

@register.inclusion_tag('creo/field-editor.html', takes_context=True)
def CreoFieldEditor(context):
    fname = context['field'].name
    c = Context({
        'ng': LalaNgScope('creo'),
    })
    c.update(context)
    return c


@register.inclusion_tag('creo/field.html', takes_context=True)
def CreoField(context, fieldName, fieldTag=None):
    c = Context({
        'field': LalaField(context['creo'], fieldName),
        'fieldTag': fieldTag,
    })
    c.update(context)
    return c


