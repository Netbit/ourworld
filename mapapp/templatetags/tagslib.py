from django import template
from mapapp.models import Comment, Construction


register = template.Library()

@register.filter
def strip(val):
    return val.replace(" Nam", "")

@register.inclusion_tag('comments.html')
def display_comments(object_id):
    con = Construction.objects.get(id__exact=object_id)
    comments = Comment.objects.filter(construction = con).order_by('-comment_date')
    return { 'comments': comments }

@register.filter
def nickname(email):
    return email.split('@')[0]