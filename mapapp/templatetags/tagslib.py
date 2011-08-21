from django import template


register = template.Library()

@register.filter
def no_answer(val):
    pass