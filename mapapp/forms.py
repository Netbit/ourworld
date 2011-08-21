from django import forms

class SearchBox(forms.Form):
    place = forms.CharField(max_length = 100)
    
class SearchPath(forms.Form):
    from_place = forms.CharField(max_length = 100)
    to_place = forms.CharField(max_length = 100)