from django.test import TestCase, RequestFactory
from manager.engine import Engine
from clean.models import Upload, Document, HeaderPreference, Header
from clean.forms.form import HeaderForm, UploadForm
from clean.views import success_view
from shutil import copyfile
import os

from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

class TestExperiment(TestCase):
    def setUp(self):
        print("setup")
        self.factory = RequestFactory()
        self.request = self.factory.get(success_view)
        self.dataIdStart = 1
  
    def test_base_clean(self):
        for i in range(3):
            performTest(0, getDataArr(0, self.dataIdStart), "Base", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(1, getDataArr(0, self.dataIdStart), "Base", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(2, getDataArr(0, self.dataIdStart), "Base", i, self.request)
            self.dataIdStart += 5

    def test_1_remove_null_clean(self):
        for i in range(3):
            performTest(0, getDataArr(1, self.dataIdStart), "One", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(1, getDataArr(1, self.dataIdStart), "One", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(2, getDataArr(1, self.dataIdStart), "One", i, self.request)
            self.dataIdStart += 5

    def test_2_remove_null_dirty(self):
        for i in range(3):
            performTest(3, getDataArr(2, self.dataIdStart), "Two", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(4, getDataArr(2, self.dataIdStart), "Two", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(5, getDataArr(2, self.dataIdStart), "Two", i, self.request)
            self.dataIdStart += 5

    def test_3_replace_null_avg_dirty(self):
        for i in range(3):
            performTest(3, getDataArr(3, self.dataIdStart), "Three", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(4, getDataArr(3, self.dataIdStart), "Three", i, self.request)
            self.dataIdStart += 5
        for i in range(3):
            performTest(5, getDataArr(3, self.dataIdStart), "Three", i, self.request)
            self.dataIdStart += 5



def performTest(filePosition, dataArr, testID, testNumber, request):
    files = [
            "10000RowClean.csv", "100000RowClean.csv", "1000000RowClean.csv",
            "10000RowDirty.csv", "100000RowDirty.csv", "1000000RowDirty.csv"
            ]

    sourceFile = os.path.abspath("uploads/testdata/" + files[filePosition])
    destinationFile = os.path.abspath("uploads/testfileresults/" + "Pos" + str(filePosition) + "ID" + testID + "TestNumber" + str(testNumber) + "." + files[filePosition])
    copyfile(sourceFile, destinationFile)
    d = destinationFile
    upload = Upload.objects.create()
    document = Document.objects.create(file=d, is_wrangled=False, upload=upload)
    engine = Engine(spark=spark, fileModel=document)
    columns = engine.getColumnNames()
    headerSaver(document,engine)


    for data in dataArr:
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

def getDataArr(testNumber, testid):
    if testNumber == 0:
        #all fields are deselected
        dataArr = [{
          "id":testid,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid + 1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid + 2,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid + 3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid + 4,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]

    elif testNumber == 1 or testNumber == 2:
        #removes null values from ID 5
        dataArr = [{
          "id":testid,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': 'nothing',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': 'nothing',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': 'nothing',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 3:
        #replace null with average on ID 4 and 5
        dataArr = [{
          "id":testid,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': 'nothing',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': 'nothing',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': 'nothing',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
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
          "id":testid,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
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
          "id":testid,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
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
          "id":testid,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]
    elif testNumber == 7:
        dataArr = [{
          "id":testid,
          "selected":True,
          'null_num': 'nothing',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+1,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+2,
          "selected":True,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          {
          "id":testid+3,
          "selected":False,
          'null_num': '',
          'replace_num': '',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },
          { 
          "id":testid+4,
          "selected":True,
          'null_num': 'replace',
          'replace_num': 'Avg',
          'null_string': '',
          'replace_string': '',
          'null_date': '',
          'replace_date': '',
          },]

    return dataArr
