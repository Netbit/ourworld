from django import forms
from django.utils.translation import ugettext_lazy as _

class CommentForm(forms.Form): 
    email = forms.EmailField(label = _('Email'), widget=forms.TextInput(attrs={'placeholder': 'john.doe@email.com'}))
    content = forms.CharField(label = _('Content'), widget=forms.Textarea(attrs={'placeholder': _('Your comment here...')}))   
    
