from pyspark.sql import SparkSession, functions as F

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
            pass
            #todo: call function that reads xml document- one below doesnt work!!!
            #self.dataframe = spark.read.format('xml').load(filePath)

    def printTable(self):
        self.dataframe.show()

    def getColumnNames(self):
        return self.dataframe.columns

    def flattenJSON(self):
        pass

test = engine('sample2.json', '.json')

test.dataframe.show()

test.dataframe.printSchema()

#collapses the streetaddress attribute from the nested address attribute
#test.dataframe.withColumn('address', F.col('address').getField('streetAddress')).show()

#convert value in address that is a struct into a dict 
address = test.dataframe.collect()[0][0].asDict()
print(address)

