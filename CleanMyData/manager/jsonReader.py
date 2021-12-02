from pyspark.sql import SparkSession, functions as F, types as T

class jsonReader:
    def __init__(self, spark, dataframe):
        self.spark = spark
        self.dataframe = dataframe

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

spark = SparkSession.builder.getOrCreate()

test = jsonReader(spark, spark.read.option("multiline","true").json("sample2.json"))

test.dataframe.show()
#print([tuple(address.values())])
#newDF = test.dataframe.collect()[0]
#newDF = spark.createDataFrame([tuple(address.values())], list(address.keys()))
#test.dataframe = test.dataframe.join(newDF)
#test.dataframe = test.dataframe.drop('address')
#test.dataframe.show()
