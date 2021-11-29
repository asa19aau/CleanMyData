from pyspark.sql import SparkSession, types as T, functions as F
import xmlReader

spark = SparkSession.builder.appName('engine').getOrCreate()

class engine:
    def __init__(self, filePath, fileType):
        if fileType == '.csv':
            self.dataframe = spark.read.csv(filePath, header=True, inferSchema=True)
        elif fileType == '.json':
            self.dataframe = spark.read.option("multiline","true").json(filePath)
            self.dataframes = self.findJSONDataframes()
        elif fileType == '.tsv':
            self.dataframe = spark.read.option("delimiter", "\t").csv(filePath, header=True)
        elif fileType == '.xml':
            reader = xmlReader.xmlReader(spark)
            self.dataframe = reader.getXMLDataFrame(filePath)
    
    def findJSONDataframes(self):
        dataframesInDocument = []
        columns = self.dataframe.columns
        for col in columns:
            if isinstance(self.dataframe[col][1], T.Row):
                print('hello')
        return 1

test = engine('sample2.json', '.json')

test.dataframe.show()
print(test.dataframe.collect()[0][5])
test.dataframe.printSchema()

#convert value in address that is a struct into a dict 
address = test.dataframe.collect()[0][0].asDict()

print(type(test.dataframe.collect()[0][5]))
print(type(test.dataframe.collect()[0][0]))

#print([tuple(address.values())])
#newDF = test.dataframe.collect()[0]
#newDF = spark.createDataFrame([tuple(address.values())], list(address.keys()))
#test.dataframe = test.dataframe.join(newDF)
#test.dataframe = test.dataframe.drop('address')
#test.dataframe.show()
