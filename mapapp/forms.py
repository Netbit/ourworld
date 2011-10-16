from django import forms
from django.utils.translation import ugettext_lazy as _

class CommentForm(forms.Form): 
    email = forms.EmailField(label = _('Email'))
    content = forms.CharField(label = _('Content'), widget=forms.Textarea())   
    
