from re import sub
from django.http.response import HttpResponse
from django.shortcuts import render
from manager.fileWriter import fileWriter
from manager.engine import Engine
from clean.forms.form import HeaderForm, UploadForm
from clean.models import Upload, Document, HeaderPreference, Header
from django.http import HttpResponseRedirect

from os import listdir
from django.conf import settings    

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession


spark = SparkSession.builder.appName('preferences').getOrCreate()


def frontpage_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            upload = Upload.objects.create()

            documents = request.FILES.getlist('documents')
            for d in documents:
                document = Document.objects.create(file=d, is_wrangled=False, upload=upload)

                #MAKE HEADER OBJECTS
                engine = Engine(spark=spark, fileModel=document)
                columns = engine.getColumnNames()

                for header in columns:
                    header_object = Header.objects.create(name=header, document=document, selected=True, type=dict(engine.dataframe.dtypes)[header])
                    header_definition = HeaderPreference.objects.create(header=header_object)
                    header_definition.save()
                    header_object.save()

            documents = Document.objects.filter(upload=upload).order_by('id')

            return HttpResponseRedirect("/header-choices/" + str(documents[0].id)) 
    else:
        form = UploadForm()
        
    return render(request, "entry.html", {
        "form": form
    })
    

def success_view(request):
    uploads = Upload.objects.all()

    #DO THIS ASYNC PLEASE
    for upload in uploads:
        documents = Document.objects.filter(upload=upload)
        for document in documents:
            if document.is_wrangled == False:
                engine = Engine(spark, document)
                engine.cleanMyData()
                document.is_wrangled = True
                document.save()

    uploads = Upload.objects.all().order_by('-id')
    
    return render(request, "success.html", {
        "uploads": uploads,
        "total_documents": Document.objects.all().count(),
    })
    
      
def headerChoice_view(request, pk):
    headers = Header.objects.filter(document_id=pk)
    
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

                if data['null_string'] == 'replace':
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
    
    document = Document.objects.get(id = pk) #Retrieve currently selected document
    upload = Upload.objects.get(documents = document) #Retrieve the Upload which the document is attached to
    documents = Document.objects.filter(upload = upload) #Retrieve all the documents of the Upload

    next_document = False

    for document in documents: 
        if document.id == pk:
            if document != documents.last():
                next_document = document.id + 1

    return render(request, "header_choices.html", {
        "form": form,
        "header_list": headers,
        "file_id": pk,
        "document": Document.objects.get(id=pk),
        "next_document": next_document
    })

    
def help_view(request):
    return render(request, "help.html")

def merge_view(request):

    if request.method == 'POST':
        documents = request.POST.getlist('document')

        if len(documents) <= 1:
            return HttpResponseRedirect("/success/")

        obj = Document.objects.filter(id__in=documents).order_by('-id')

        return render(request, "merge_files.html", {
            "documents": obj,
        })

    return HttpResponseRedirect("/success/")


def find_filenames( path_to_dir, suffix ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


def merge_documents_view(request, pk):
    if request.method == 'POST':
        document = Document.objects.get(id=pk)
        upload = document.upload
        documents = upload.documents

        header_relations = request.POST.getlist('relation')
    
        engines = []

        for docu in documents.all():
            if docu is not document:
                engines.append(Engine(spark, docu))
        
        dataframes = []

        subscribing_header = []

        for rel in header_relations:
            if rel != 'none':
                master_header = Header.objects.get(id=int(rel.split(':')[0]))
                subscribing_header = Header.objects.get(id=int(rel.split(':')[1]))
                
        for engine in engines:
            print(engines)
            if engine.dataframe not in dataframes:
                dataframes.append(engine.dataframe.withColumnRenamed(subscribing_header.name, master_header.name))

        unified_data = engines[0].dataframe

        for data in dataframes[1:]:
            unified_data = unified_data.union(data)

        fileWriter(spark=spark, filePath='merged', fileExtension=engines[0].document.file_extension, dataframe=unified_data)
        merged_files = find_filenames('merged', engines[0].document.file_extension)
        file_to_send = open("merged/" + merged_files[-1], "r")
        
        response = HttpResponse(file_to_send)
        response['Content-Disposition'] = 'attachment; filename="' + merged_files[-1] + '"'
        return response

    return HttpResponseRedirect("/success/")


def download_view(request, pk):
    document = Document.objects.get(id=pk)

    merged_files = find_filenames(document.file_path + '/', document.file_extension)
    file_to_send = open(document.file_path + '/' + merged_files[-1], "r")

    response = HttpResponse(file_to_send)
    response['Content-Disposition'] = 'attachment; filename="' + merged_files[-1] + '"'
    return response


