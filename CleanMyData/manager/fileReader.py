from .jsonReader import *
from .xmlReader import *

def fileReader(spark, filePath, fileExtension):
    if fileExtension == '.csv':
        dataframe = spark.read.csv(filePath, header=True, inferSchema=True)
    elif fileExtension == '.orc':
        dataframe = spark.read.orc(filePath)
    elif fileExtension == '.parquet':
        dataframe = spark.read.parquet(filePath)
    elif fileExtension == '.json':
        #reader = jsonReader()
        dataframe = spark.read.option("multiline","true").json(filePath)
        #dataframes = reader.findJSONDataframes()
    elif fileExtension == '.tsv':
        dataframe = spark.read.option("delimiter", "\t").csv(filePath, header=True)
    elif fileExtension == '.xml':
        reader = xmlReader(spark)
        dataframe = reader.getXMLDataFrame(filePath)

    return dataframe
