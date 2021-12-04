import pyspark.pandas as pan

def fileWriter(spark, filePath, fileExtension, dataframe):
    panDf = dataframe.toPandas()
    print(filePath)
    if fileExtension == '.csv':
        panDf = dataframe.toPandas()
        panDf.to_csv(filePath)
    elif fileExtension == '.orc':
        dataframe.to_orc(filePath)
    elif fileExtension == '.parquet':
        dataframe.to_parquet(filePath)
    elif fileExtension == '.json':
        panDf.to_json(filePath)

