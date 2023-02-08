from django import template


register = template.Library()


@register.filter(name='setVar')
def setVar(value, arg):
    return value.replace(arg, '')
