from pyspark.sql import SparkSession, functions as F, types as T
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
        dataframesInDocument = [self.dataframe]
        columns = self.dataframe.columns
        for x in range(len(self.dataframe.columns)):
            name = self.dataframe.dtypes[x][0]
            Type = self.dataframe.schema[x].dataType
            if isinstance(Type, T.StructType):
                nestedDFColNames = Type.fieldNames()
                newDataframe = spark.createDataFrame([], Type)
                testDF = self.dataframe.withColumn(name, F.from_json(self.dataframe[x], T.MapType(T.StringType(), T.MapType.jsonValue())))
                testDF.show()
            
        return dataframesInDocument

test = engine('sample2.json', '.json')

test.dataframe.show()
#print([tuple(address.values())])
#newDF = test.dataframe.collect()[0]
#newDF = spark.createDataFrame([tuple(address.values())], list(address.keys()))
#test.dataframe = test.dataframe.join(newDF)
#test.dataframe = test.dataframe.drop('address')
#test.dataframe.show()
