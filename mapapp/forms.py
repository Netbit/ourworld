from django import forms
from mapapp.models import Comments

class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comments
        exclude = ("comment_date",)
    
