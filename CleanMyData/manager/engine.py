from pyspark.sql import SparkSession, functions as F, types as T
import xmlReader
import jsonReader
#import modules.module as module

spark = SparkSession.builder.appName('engine').getOrCreate()

class engine:
    def __init__(self, spark, fileModel):
        self.spark = spark
        
        self.fileModel = fileModel

        if self.fileModel.file_extension == '.csv':
            self.dataframe = self.spark.read.csv(self.fileModel.file_path, header=True, inferSchema=True)
        elif self.fileModel.file_extension == '.orc':
            self.dataframe = self.spark.read.orc(self.fileModel.file_path)
        elif self.fileModel.file_extension == '.parquet':
            self.dataframe = self.spark.read.parquet(self.fileModel.file_path)
        elif self.fileModel.file_extension == '.json':
            reader = jsonReader()
            self.dataframe = self.spark.read.option("multiline","true").json(self.fileModel.file_path)
            self.dataframes = self.reader.findJSONDataframes()
        elif self.fileModel.file_extension == '.tsv':
            self.dataframe = self.spark.read.option("delimiter", "\t").csv(self.fileModel.file_path, header=True)
        elif self.fileModel.file_extension == '.xml':
            reader = xmlReader.xmlReader(self.spark)
            self.dataframe = reader.getXMLDataFrame(self.fileModel.file_path)

    def __init__(self, spark, filePath, fileType):
        #for testing purposes
        self.spark = spark

        if fileType == '.csv':
            self.dataframe = self.spark.read.csv(filePath, header=True, inferSchema=True)
        elif fileType == '.orc':
            self.dataframe = self.spark.read.orc(filePath)
        elif fileType == '.parquet':
            self.dataframe = self.spark.read.parquet(filePath)
        elif fileType == '.json':
            self.dataframe = self.spark.read.option("multiline","true").json(filePath)
            #self.dataframes = self.findJSONDataframes()
        elif fileType == '.tsv':
            self.dataframe = self.spark.read.option("delimiter", "\t").csv(filePath, header=True)
        elif fileType == '.xml':
            reader = xmlReader.xmlReader(self.spark)
            self.dataframe = reader.getXMLDataFrame(filePath)

    def getColumnNames(self):
        return self.dataframe.columns

    def getSchema(self):
        return self.dataframe.schema

    def cleanMyData(self):
        for header in fileModel.headers:
            if header.header_preference.current_type == 'non':
                pass
            elif header.header_preference.current_type == 'Temperature':
                pass
            elif header.header_preference.current_type == 'Distance':
                pass
            elif header.header_preference.current_type == 'Weight':
                pass
            else:
                pass


