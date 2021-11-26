from pyspark.sql import SparkSession
import re

class xmlReader:
    def __init__(self, spark):
        self.spark = spark
        self.headerRe = re.compile("<[a-zA-Z]*\/?>")
        self.valueRe = re.compile(">.*\/?<")
        self.matchArr = []
        self.valueArr = []
        self.header = []
        self.values = []
        self.valueTuples = []
        self.valueTupleArr = []
        self.readFlag = False
    #can maybe look for a way of doing things, that doesn't require this many arrays

    def getXMLHeader(self, filePath):
        """opens the file and extracts the header/column names as an array"""
        with open(filePath) as f:
            line = f.readline()
            while line:
                line = f.readline()

                #finds the point where a row ends and breaks after the first row ends
                if line.strip() == "</row>":
                    self.readFlag = False
                    break

                #finds the column names from a row and appends them to a list
                if self.readFlag == True and line.strip() != "":
                    self.matchArr.append(self.headerRe.findall(line))

                #finds the point where a row starts
                if line.strip() == "<row>":
                    self.readFlag = True

        #puts the values into a one dimensional array from the original two dimensional array
        for match in self.matchArr:
            match[0] = match[0].replace("<", "").replace(">", "").replace("/", "")
            self.header.append(match[0])

    def getXMLvalues(self, filePath, amountOfColumns):
        """Opens the file and extracts all values for each row. Each row is put into an array, with each row being in the form of a tuple"""
        with open(filePath) as f:
            line = f.readline()
            while line:
                line = f.readline()

                #finds the point where a row ends
                if line.strip() == "</row>":
                    self.readFlag = False

                #adds values to a list of values
                if self.readFlag == True and line.strip() != "":
                    self.valueArr.append(self.valueRe.findall(line))

                #finds the point where a row starts
                if line.strip() == "<row>":
                    self.readFlag = True
        for value in self.valueArr:

            #handles null fields
            if not value:
                self.values.append("")

            #removes xml formatting
            else:
                value[0] = value[0].replace("<", "").replace(">", "")
                self.values.append(value[0])

        #takes the array of elements and puts them into an array of tuples, with one tuple representing a row
        for i in range(1, int(len(self.values)/amountOfColumns)):
            for x in range(amountOfColumns):
                self.valueTuples.append(self.values[x*i])
            self.valueTupleArr.append(tuple(self.valueTuples))
            self.valueTuples = []

    def getXMLDataFrame(self, filePath):
        """Calls the getXMLHeader and getXMLvalues functions to create a spark dataframe. Returns the spark dataframe."""
        self.getXMLHeader(filePath)
        self.getXMLvalues(filePath, len(self.header))
        df = spark.createDataFrame(self.valueTupleArr, self.header)

        return df

