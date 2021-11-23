import pyspark.pandas as pan
#Calculate average of a column

def calculateAverage(dataFrame: pan.DataFrame):
    return dataFrame.mean()

