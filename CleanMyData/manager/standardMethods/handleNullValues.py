import pyspark.pandas as pan, average, median
import os

def deleteNullValues(dataFrame: pan.DataFrame):
    return dataFrame.dropna(axis=0)

def replaceNullWithAverage(dataFrame: pan.DataFrame):
    return  dataFrame.fillna(value=average.calculateAverage(dataFrame), axis=0)

def replaceNullWithMedian(dataFrame: pan.DataFrame):
    return  dataFrame.fillna(value=median.calculateMedian(dataFrame), axis=0)

