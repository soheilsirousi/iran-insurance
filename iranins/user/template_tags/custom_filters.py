from django import template

register = template.Library()

@register.filter(name='abs', is_safe=True)
def abs(value):
    return abs(value)
