import pyspark.pandas as pan
#Calculate median from column values

def calculateMedian(dataFrame: pan.DataFrame):
    return dataFrame.median()

