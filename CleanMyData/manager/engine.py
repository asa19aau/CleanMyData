from pyspark.sql import SparkSession, functions as F
import xmlReader
import re

spark = SparkSession.builder.appName('engine').getOrCreate()

class engine:
    def __init__(self, filePath, fileType):
        if fileType == '.csv':
            self.dataframe = spark.read.csv(filePath, header=True, inferSchema=True)
        elif fileType == '.json':
            self.dataframe = spark.read.option("multiline","true").json(filePath)
        elif fileType == '.tsv':
            self.dataframe = spark.read.option("delimiter", "\t").csv(filePath, header=True)
        elif fileType == '.xml':
            reader = xmlReader.xmlReader(spark)
            self.dataframe = reader.getXMLdataframe(filePath)

    def getColumnNames(self):
        return self.dataframe.columns

    def flattenJSON(self, df):
        #find which columns has nested values
        columnTypes = df.dtypes
        for col in columnTypes:
            if columnTypes[col] == 'struct<>'


test = engine('sample2.json', '.json')

test.dataframe.show()
print(type(test.dataframe.collect()[0][0]))
test.dataframe.printSchema()

test.flattenJSON(test.dataframe)

#convert value in address that is a struct into a dict 
address = test.dataframe.collect()[0][0].asDict()
print(address)

print(type(address.keys()))

print([tuple(address.values())])
newDF = test.dataframe.collect()[0]
newDF = spark.createDataFrame([tuple(address.values())], list(address.keys()))
test.dataframe = test.dataframe.join(newDF)
test.dataframe = test.dataframe.drop('address')
test.dataframe.show()
