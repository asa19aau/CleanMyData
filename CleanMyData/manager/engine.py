from pyspark.sql import DataFrame
from clean.models import File, Header
from .fileReader import *
#from CleanMyData.clean.models import File
#import modules.module as module


class Engine:
    def __init__(self, spark, fileModel):
        self.spark = spark
        
        self.file = fileModel

        self.dataframe = fileReader(self.spark, self.file.file_path, self.file.file_extension)


    def getColumnNames(self):
        return self.dataframe.columns


    def getSchema(self):
        return self.dataframe.schema


    def cleanMyData(self):
        #TODO: add logic when modules can be merged
        file_headers = Header.objects.filter(file=self.file)
        for header in file_headers:
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
            firstDataframe = fileReader(self.spark, firstFile.file_path, firstFile.file_extension)

        if isinstance(secondFile, DataFrame):
            secondDataframe = secondFile
        elif firstFile != None:
            secondDataframe = fileReader(self.spark, secondFile.file_path, secondFile.file_extension)

        print(firstDataframe.count(), secondDataframe.count())

        if len(firstDataframe.columns) == len(secondDataframe.columns):
            return firstDataframe.union(secondDataframe)


    def joinDataframes(self, firstFile, secondFile, joinOn):
        if isinstance(firstFile, DataFrame):
            firstDataframe = firstFile
        elif firstFile != None:    
            firstDataframe = fileReader(self.spark, firstFile.file_path, firstFile.file_extension)

        if isinstance(secondFile, DataFrame):
            secondDataframe = secondFile
        elif firstFile != None:
            secondDataframe = fileReader(self.spark, secondFile.file_path, secondFile.file_extension)

        return firstDataframe.join(secondDataframe, on=joinOn, how='fullouter')

