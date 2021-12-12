from django.test import TestCase, RequestFactory
from manager.engine import Engine
from clean.models import Upload, Document, HeaderPreference, Header
from clean.forms.form import HeaderForm, UploadForm
from clean.views import success_view
from shutil import copyfile
import os

from pyspark import SparkContext
from pyspark.sql import SparkSession

test = []

spark = SparkSession.builder.getOrCreate()

class TestExperiment(TestCase):
    def setUp(self):
        print("setup")
        self.factory = RequestFactory()
        self.request = self.factory.get(success_view)
        self.upload = Upload.objects.create()
        self.d = "testdata/100000rowsdirty.csv"
    
    def test_data_wrangling(self):
        return
        print("test_data_wrangling")
        upload = Upload.objects.create()
        document = Document.objects.create(file=self.d, is_wrangled=False, upload=upload)
        engine = Engine(spark=spark, fileModel=document)
        columns = engine.getColumnNames()
        headerSaver(document, engine)
        request = self.factory.get(success_view)
        #print(f"request: {request}")
        response = success_view(request)
        #print(f"response: {response}")
        headers = Header.objects.filter(document_id=1)
        #print(f"headers: {headers}")
   
    def test_1000rows_clean(self):
        performTest(0, getDataArr(0), "Base", 1, self.request)
        performTest(0, getDataArr(1), "1", 1, self.request)

def performTest(filePosition, dataArr, testID, testNumber, request):
    files = [
            "set1.csv", "set2.csv", "set3.csv",
            "set4.csv", "set5.csv", "set6.csv"
            ]

    sourceFile = os.path.abspath("uploads/testdata/" + files[filePosition])
    destinationFile = os.path.abspath("uploads/testfileresults/" + "Pos" + str(filePosition) + "ID" + testID + "TestNumber" + str(testNumber) + files[filePosition])
    copyfile(sourceFile, destinationFile)
    d = destinationFile
    upload = Upload.objects.create()
    document = Document.objects.create(file=d, is_wrangled=False, upload=upload)
    engine = Engine(spark=spark, fileModel=document)
    columns = engine.getColumnNames()
    headerSaver(document,engine)


    #find a way to set preferences below here
    for data in dataArr:
        #print(f"data in tester: {data}---------------------------------")

        header = Header.objects.get(id=data['id'])
        header.selected = data['selected']
        #print(f"header.selected: {header.selected} ==================")
    
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
    response = success_view(request)
    headers = Header.objects.filter(document_id=1)
 

def headerSaver(document, engine):
    columns = engine.getColumnNames()
    for header in columns:
        header_object = Header.objects.create(name=header, document=document, selected=True, type=dict(engine.dataframe.dtypes)[header])
        header_definition = HeaderPreference.objects.create(header=header_object)
        header_definition.save()
        header_object.save()

def getDataArr(testNumber):
    if testNumber == 0:
        dataArr = [{
          "id":1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]

    elif testNumber == 1:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 2:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 3:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 4:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 5:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 6:
        dataArr = [{
          "id":1,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":3,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":5,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]






   

    return dataArr
