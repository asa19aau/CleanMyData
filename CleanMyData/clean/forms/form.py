from django import forms
from clean.choices import *

class UploadForm(forms.Form):
    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
                
class HeaderForm(forms.Form):
    id = forms.IntegerField()

    selected = forms.BooleanField(required=False)

    # Handling of null in num
    null_num = forms.CharField(max_length=30, required=False)
    replace_num = forms.CharField(max_length=30, required=False)


    # Handling of null in string
    null_string = forms.CharField(max_length=30, required=False)
    replace_string = forms.CharField(max_length=30, required=False)

    # Handling of null in date
    null_date = forms.CharField(max_length=30, required=False)
    replace_date = forms.CharField(max_length=30, required=False)



