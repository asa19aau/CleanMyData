from django.http.response import HttpResponse
from django.shortcuts import render
from manager.engine import Engine
from clean.forms.form import HeaderForm
from clean.models import File, HeaderPreference, Header
from clean.forms.form import FileForm
from django.http import HttpResponseRedirect

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession


spark = SparkSession.builder.appName('preferences').getOrCreate()


def frontpage_view(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        
        if form.is_valid():
            file_form = form.save()

            #MAKE HEADER OBJECTS
            engine = Engine(spark=spark, fileModel=file_form)
            columns = engine.getColumnNames()
            print(engine.getSchema())
            
            for header in columns:
                header_object = Header.objects.create(name=header, file=file_form, selected=True, type=dict(engine.dataframe.dtypes)[header]) #type=dict(df.dtypes)[header]  |  num, string, date
                header_definition = HeaderPreference.objects.create(header=header_object)
                header_definition.save()
                header_object.save()
            
            return HttpResponseRedirect("/header-choices/" + str(file_form.id)) 
    else:
        form = FileForm()
        
    return render(request, "entry.html", {
        "form": form
    })
    

def success_view(request):
    files = File.objects.all()

    #DO THIS ASYNC PLEASE
    for file in files:
        if file.is_wrangled == False:
            engine = Engine(spark, file)
            engine.cleanMyData()
            file.is_wrangled = True
            file.save()

    files = File.objects.order_by('-id')
    return render(request, "success.html", {
        "files": files
    })
    
      
def headerChoice_view(request, pk):
    headers = Header.objects.filter(file_id=pk)
    
    if request.method == 'POST':
        form = HeaderForm(request.POST)
        
        if form.is_valid():
            data = {
                "id": form.cleaned_data['id'],
                "selected": form.cleaned_data['selected'],
                'null_num': form.cleaned_data['null_num'],
                'replace_num': form.cleaned_data['replace_num'],
                'null_string': form.cleaned_data['null_string'],
                'replace_string': form.cleaned_data['replace_string'],
                'null_date': form.cleaned_data['null_date'],
                'replace_date': form.cleaned_data['replace_date'],
            }
            
            header = Header.objects.get(id=data['id'])
            print(header.header_preference.null_choice_string)
            header.selected = data['selected']

            if data['null_num'] != '':
                if data['replace_num'] != 'replace':
                    header.header_preference.null_choice_num = data['null_num']
                    data['replace'] = ''

                if data['null_num'] == 'replace':
                    header.header_preference.null_choice_num = data['replace_num']

                else:
                    data['null_num'] = None

            if data['null_string'] != '':
                if data['replace_string'] != 'replace':
                    header.header_preference.null_choice_string = data['null_string']
                    data['replace_string'] = ''

                if data['null_string'] != 'replace':
                    header.header_preference.null_choice_string = data['replace_string']

                else:
                    data['null_string'] = None

            if data['null_date'] != '':
                if data['replace_date'] != 'replace':
                    header.header_preference.null_choice_date = data['null_date']
                    data['replace'] = ''

                if data['null_date'] == 'replace':
                    header.header_preference.null_choice_date = data['replace_date']

                else:
                    data['null_date'] = None

            header.header_preference.save()
            header.save()
            
            return HttpResponseRedirect("/header-choices/" + str(pk)) 
    else:
        form = HeaderForm()
    
    return render(request, "header_choices.html", {
        "form": form,
        "header_list": headers,
        "file_id": pk
    })

    
def help_view(request):
    return render(request, "help.html")
