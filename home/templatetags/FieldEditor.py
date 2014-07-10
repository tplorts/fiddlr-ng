from django import template

register = template.Library()

class FEField():
    def __init__(self, name):
        self.name = name

class FENgScope():
    def __init__(self, thingVarName):
        self.thing = thingVarName

@register.inclusion_tag('profiles/field-editor.html')
def FieldEditor( fieldName ):
    return {
        'ng': FENgScope('thing'),
        'field': FEField(fieldName),
    }
