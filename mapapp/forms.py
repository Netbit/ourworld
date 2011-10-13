from django import forms
from mapapp.models import Comment

class CommentForm(forms.ModelForm):    
    class Meta:
        model = Comment
        exclude = ("comment_date", "construction")
    
