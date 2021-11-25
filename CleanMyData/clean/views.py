from django.http.response import HttpResponse
from django.shortcuts import render
from clean.forms.form import HeaderForm
from clean.models import File, Preferences, Header
from clean.forms.form import FileForm
from django.http import HttpResponseRedirect

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession


def frontpage_view(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.save()
            
            #MAKE HEADER OBJECTS
            spark = SparkSession.builder.appName('preferences').getOrCreate()
            df = spark.read.csv(str(file.file_path), header=True)
            header_list = df.columns
            
            for header in header_list:
                header_object = Header.objects.create(name=header, file=file, selected=True)
                header_object.save()
                            
            #MAKE PREFERENCE OBJECT
            file_preferences = Preferences.objects.create(file=file)
            file_preferences.save()
            
            return HttpResponseRedirect("/header-choices/" + str(file.id)) 
    else:
        form = FileForm()
        

    return render(request, "entry.html", {
        "form": form
    })
    

def success_view(request):
    files = File.objects.order_by('id')
    return render(request, "success.html", {
        "files": files
    })
    

def preferences_view(request, pk):
    preferences = Preferences.objects.get(id=pk)
    
    return render(request, "preferences.html", {

      
def headerChoice_view(request, pk):
    headers = Header.objects.filter(file_id=pk)
    
    if request.method == 'POST':
        form = HeaderForm(request.POST)
        
        if form.is_valid():
            header_id = form.cleaned_data['id']
            header_selected = form.cleaned_data['selected']
            header = Header.objects.get(id=header_id)
            header.selected = header_selected
            header.save()
            
            return HttpResponseRedirect("/header-choices/" + str(pk)) 
    else:
        form = HeaderForm()
    
    return render(request, "header_choices.html", {
        "form": form,
        "header_list": headers
    })
    

def help_view(request):
    return render(request, "help.html")

