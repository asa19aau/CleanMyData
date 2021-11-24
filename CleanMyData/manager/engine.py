from pyspark.sql import SparkSession

class engine:
    def __init__(self, filePath, fileType):
        spark = SparkSession.builder.getOrCreate()
        if fileType == '.csv':
            self.dataframe = spark.read.csv(filePath, header=True)
        elif filetype == '.json':
            self.dataframe = spark.read.json(filePath)
        elif filetype == '.tsv':
            self.dataframe = spark.read.option("delimiter", "\t").csv(filePath, header=True)
        elif filetype == '.xml':
            self.dataframe = spark.read.xml(filePath)

    def getColumnNames(self):
        return self.dataframe.columns

test = engine('GlobalTemperatures.csv')
