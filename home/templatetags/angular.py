from django import template

register = template.Library()


@register.inclusion_tag('tags/angular.html')
def angular( *args, **kwargs ):
    if 'version' not in kwargs:
        kwargs['version'] = '1.3.0-beta.13'
    return kwargs

@register.inclusion_tag('tags/angular-app.html')
def angular_app( app_directory ):
    return {'app_directory': app_directory}
