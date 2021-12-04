import pyspark.pandas as pan
from .average import *
from .median import *

def deleteNullValues(dataFrame: pan.DataFrame, headerName):
    return dataFrame.dropna(axis=0, subset=headerName)

def replaceNullWithAverage(dataFrame: pan.DataFrame):
    return  dataFrame.fillna(value=calculateAverage(dataFrame), axis=0)

def replaceNullWithMedian(dataFrame: pan.DataFrame):
    return  dataFrame.fillna(value=calculateMedian(dataFrame), axis=0)
