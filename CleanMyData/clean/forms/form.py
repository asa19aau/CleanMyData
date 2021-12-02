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
    selected = forms.BooleanField(required=False)
    id = forms.IntegerField()

class HeaderDefinitionForm(ModelForm):
    id = forms.IntegerField()

    class Meta: 
        model = HeaderPreference
        fields = ('current_type', 'desired_type',)


