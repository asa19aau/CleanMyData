from django import forms
from django.forms import ModelForm, ClearableFileInput
from clean.models import HeaderPreference
from clean.models import Header
from clean.models import File
from clean.choices import *

class FileForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta: 
        model = File
        fields = '__all__'
        
        
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



