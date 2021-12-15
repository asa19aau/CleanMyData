import pyspark.pandas as pan

def fileWriter(spark, filePath, fileExtension, dataframe):
    if fileExtension == '.csv':
        dataframe.repartition(1).write.mode("overwrite").csv(filePath, header=True)
    elif fileExtension == '.orc':
        dataframe.repartition(1).write.mode("overwrite").orc(filePath)
    elif fileExtension == '.parquet':
        dataframe.repartition(1).write.mode("overwrite").parquet(filePath)
    elif fileExtension == '.json':
        dataframe.repartition(1).write.mode("overwrite").json(filePath)

