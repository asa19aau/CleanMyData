from pyspark.sql import SparkSession

class engine:
    def __init__(self, filePath, fileType):
        spark = SparkSession.builder.getOrCreate()
        if fileType == '.csv':
            self.dataframe = spark.read.csv(filePath, header=True)
        elif fileType == '.json':
            self.dataframe = spark.read.option("multiline","true").json(filePath)
        elif fileType == '.tsv':
            self.dataframe = spark.read.option("delimiter", "\t").csv(filePath, header=True)
        elif fileType == '.xml':
            self.dataframe = spark.read.format('xml').load(filePath)

    def printTable(self):
        self.dataframe.show()

    def getColumnNames(self):
        return self.dataframe.columns

test = engine('employee.xml', '.xml')

test.printTable()
