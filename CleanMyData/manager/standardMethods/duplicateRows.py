import pyspark.pandas as pan

#Removes all duplicate rows
def removeEntirelyDuplicateRow(dataFrame: pan.DataFrame):
    return dataFrame.drop_duplicates()

#Removes duplicate rows based on a primary key
def removePartiallyDuplicateRow(dataFrame: pan.DataFrame, relevantColumn: int):
    return dataFrame.drop_duplicates(subset=dataFrame.column[relevantColumn])