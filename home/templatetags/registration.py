from django import template

register = template.Library()


@register.inclusion_tag('registration/signin-form.html', takes_context=True)
def SigninForm(context):
    if 'next' not in context:
        context['next'] = '/'
    return context
