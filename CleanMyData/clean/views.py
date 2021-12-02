from django.http.response import HttpResponse
from django.shortcuts import render
from clean.forms.form import HeaderDefinitionForm
from clean.forms.form import HeaderForm
from clean.models import File, HeaderPreference, Header
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
                header_definition = HeaderPreference.objects.create(header=header_object)
                header_definition.save()
                header_object.save()
            
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
        "header_list": headers,
        "file_id": pk
    })


def headerDefinition_view(request, pk):
    headers_definitions = HeaderPreference.objects.filter(header__file_id=pk, header__selected=True) 

    if request.method == 'POST':
        form = HeaderDefinitionForm(request.POST)

        if form.is_valid():
            definition_id = form.cleaned_data['id']
            definition_current = form.cleaned_data['current_type']
            definition_desired = form.cleaned_data['desired_type']
            defintion = HeaderPreference.objects.get(id=definition_id)
            print(defintion)
            defintion.current_type = definition_current
            defintion.desired_type = definition_desired
            defintion.save()
            print(defintion)
            
            return HttpResponseRedirect("/header-choices/" + str(pk) + "/definitions") 
    else:
        form = HeaderDefinitionForm()

    return render(request, "header_choices_definitions.html", {
        "forms": form,
        "header_definitions": headers_definitions,
        "file_id": pk
    })   

    
def help_view(request):
    return render(request, "help.html")

