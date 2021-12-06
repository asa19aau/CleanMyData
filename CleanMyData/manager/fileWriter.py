import pyspark.pandas as pan

def fileWriter(spark, filePath, fileExtension, dataframe):
    if fileExtension == '.csv':
        dataframe.write.mode("overwrite").csv(filePath)
    elif fileExtension == '.orc':
        dataframe.write.mode("overwrite").orc(filePath)
    elif fileExtension == '.parquet':
        dataframe.write.mode("overwrite").parquet(filePath)
    elif fileExtension == '.json':
        dataframe.write.mode("overwrite").json(filePath)

