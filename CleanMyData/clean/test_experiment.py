from django.test import TestCase, RequestFactory
from manager.engine import Engine
from clean.models import Upload, Document, HeaderPreference, Header
from clean.views import success_view

from pyspark import SparkContext
from pyspark.sql import SparkSession

test = []

spark = SparkSession.builder.getOrCreate()

class TestExperiment(TestCase):
    def setUp(self):
        print("setup")
        self.factory = RequestFactory()
        self.upload = Upload.objects.create()
        self.d = "testdata/100000rowsdirty.csv"
    
    def test_data_wrangling(self):
        print("test_data_wrangling")
        upload = Upload.objects.create()
        document = Document.objects.create(file=self.d, is_wrangled=False, upload=upload)
        engine = Engine(spark=spark, fileModel=document)
        columns = engine.getColumnNames()
        headerSaver(document, engine)
        request = self.factory.get(success_view)
        print(f"request: {request}")
        response = success_view(request)
        print(f"response: {response}")
   
    def test_1000rows_clean():
        pass

def performTest(dataPosition, prefSetting):
    data = [
            "testdata/set1.csv", "testdata/set2.csv", "testdata/set3.csv",
            "testdata/set4.csv", "testdata/set5.csv", "testdata/set6.csv"
            ]
    #find a way to set preferences below here
    prefSetting = [

            ]
    d = data[dataPosition]

def headerSaver(document, engine):
    columns = engine.getColumnNames()
    for header in columns:
        header_object = Header.objects.create(name=header, document=document, selected=True, type=dict(engine.dataframe.dtypes)[header])
        header_definition = HeaderPreference.objects.create(header=header_object)
        header_definition.save()
        header_object.save()
 
