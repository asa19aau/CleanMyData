from django import forms
from django.forms import ModelForm, ClearableFileInput
from clean.models import File

class CleanerForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta: 
        model = File
        fields = '__all__'