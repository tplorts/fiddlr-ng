from django import template
from django.template import Context

register = template.Library()


@register.inclusion_tag('fithifile/about-section.html', takes_context=True)
def FithifileAboutSection(context):
    return context


class LalaField():
    def __init__(self, thing, name, default=''):
        self.thing = thing
        self.value = getattr(thing, name)
        self.name = name
        self.defaultValue = default

class LalaNgScope():
    def __init__(self, thingVarName):
        self.thing = thingVarName

@register.inclusion_tag('fithifile/field-editor.html', takes_context=True)
def FithifileFieldEditor(context):
    fname = context['field'].name
    c = Context({
        'ng': LalaNgScope('thing'),
    })
    c.update(context)
    return c


@register.inclusion_tag('fithifile/field.html', takes_context=True)
def FithifileField(context, fieldName, fieldTag=None):
    c = Context({
        'field': LalaField(context['thing'], fieldName),
        'fieldTag': fieldTag,
    })
    c.update(context)
    return c


