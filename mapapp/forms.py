from django import forms
from django.utils.translation import ugettext_lazy as _
from captcha.fields import CaptchaField

class CommentForm(forms.Form): 
    email = forms.EmailField(label = _('Email'), widget=forms.TextInput(attrs={'placeholder': 'john.doe@email.com', 'required' : 'required'}))
    content = forms.CharField(label = _('Content'), widget=forms.Textarea(attrs={'placeholder': _('Your comment here...'), 'required' : 'required'}))
    captcha = CaptchaField('Are you human?')
    
class InputFile(forms.Form):
    data = forms.FileField(label = _('Input your file'))   
    
