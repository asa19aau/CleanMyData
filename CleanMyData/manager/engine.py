from pyspark.sql import SparkSession, DataFrame
from fileReader import *
#from CleanMyData.clean.models import File
#import modules.module as module

spark = SparkSession.builder.appName('engine').getOrCreate()

class engine:
    def __init__(self, spark, fileModel):
        self.spark = spark
        
        self.fileModel = fileModel

        self.dataframe = fileReader(self.spark, self.fileModel.file_path, self.fileModel.file_extension)

    def __init__(self, spark, filePath, fileType):
        #for testing purposes, remove when frontend and engine have been linked
        self.spark = spark

        self.dataframe = fileReader(self.spark, filePath, fileType)

    def getColumnNames(self):
        return self.dataframe.columns

    def getSchema(self):
        return self.dataframe.schema

    def cleanMyData(self):
        #TODO: add logic when modules can be merged
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

    def unifyDataframes(self, firstFile, secondFile):
        if isinstance(firstFile, DataFrame):
            firstDataframe = firstFile
        elif firstFile != None:    
            firstDataframe = filereader(self.spark, firstFile.file_path, firstFile.file_extension)

        if isinstance(secondFile, DataFrame):
            secondDataframe = secondFile
        elif firstFile != None:
            secondDataframe = filereader(self.spark, secondFilemodel.file_path, secondFilemodel.file_extension)

        print(firstDataframe.count(), secondDataframe.count())

        if len(firstDataframe.columns) == len(secondDataframe.columns):
            return firstDataframe.union(secondDataframe)

    def joinDataframes(self, firstFile, secondFile, joinOn):
        if isinstance(firstFile, DataFrame):
            firstDataframe = firstFile
        elif firstFile != None:    
            firstDataframe = filereader(self.spark, firstFile.file_path, firstFile.file_extension)

        if isinstance(secondFile, DataFrame):
            secondDataframe = secondFile
        elif firstFile != None:
            secondDataframe = filereader(self.spark, secondFilemodel.file_path, secondFilemodel.file_extension)

        return firstDataframe.join(secondDataframe, on=joinOn, how='fullouter')

