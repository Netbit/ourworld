from django import template


register = template.Library()

@register.filter
def no_answer(val):
    pass

@register.filter
def strip(val):
    return val.replace(" Nam", "")