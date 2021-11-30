import pyspark.pandas as pan
#Calculate median from column values

def replaceNullWithValue(dataFrame: pan.DataFrame, replacementValue):
    return dataFrame.fillna(replacementValue)

