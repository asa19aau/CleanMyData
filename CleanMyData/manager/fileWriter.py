import pyspark.pandas as pan

def fileWriter(spark, filePath, fileExtension, dataframe):
    if fileExtension == '.csv':
        dataframe.write.csv(filePath)
    elif fileExtension == '.orc':
        dataframe.write.orc(filePath)
    elif fileExtension == '.parquet':
        dataframe.write.parquet(filePath)
    elif fileExtension == '.json':
        dataframe.write.json(filePath)

