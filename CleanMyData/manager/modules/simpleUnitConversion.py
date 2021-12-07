import pyspark.pandas as pan
from .module import Module

class SimpleUnitConversion(Module):
    def __init(self, header, dataframe):
        super().__init__(header, dataframe)

## Temperature unit ##
    def temperatureConversion(self):
        self.dataframe = super().runCleaner()
        currentUnit = self.header.header_preference.current_type
        expectedUnit = self.header.header_preference.desired_type
        name = self.header.name
        dataframe = self.dataframe[name]
        if (currentUnit == "C") and (expectedUnit == "F"): 
            self.dataframe[name] = dataframe.mul(other=9/5).add(other=32)
        elif (currentUnit == "C") and (expectedUnit == "K"):
            self.dataframe[name] = dataframe.add(other=273.15)

        elif (currentUnit == "F") and (expectedUnit == "C"): 
            self.dataframe[name] = dataframe.sub(other=32).mul(other=(5/9))
        elif (currentUnit == "F") and (expectedUnit == "K"): 
            df = dataframe.sub(other=32).mul(other=(5/9))
            self.dataframe[name] = df.add(other=275.15)  

        elif (currentUnit == "K") and (expectedUnit == "C"): 
            self.dataframe[name] = dataframe.sub(other=273.15)
        elif (currentUnit == "K") and (expectedUnit == "F"): 
            df = dataframe.sub(other=275.15)
            self.dataframe[name] = df.mul(other=9/5).add(other=32)
        else: return
        return self.dataframe

    ## Weight unit ##
    def weightConversion(self):
        super().runCleaner()
        currentUnit = self.header.header_preference.current_type
        expectedUnit = self.header.header_preference.desired_type
        name = self.header.name
        dataframe = self.dataframe[name]
        if (currentUnit == "KG") and (expectedUnit == "LB"):
            self.dataframe[name] = dataframe.mul(other=2.20462262)
        elif (currentUnit == "LB") and (expectedUnit == "KG"):
            self.dataframe[name] = dataframe.mul(other=0.45359237)
            
        elif (currentUnit == "Gram") and (expectedUnit == "Ounce"):
            self.dataframe[name] = dataframe.mul(other=0.0352739619)
        elif (currentUnit == "Ounce") and (expectedUnit == "Gram"):
            self.dataframe[name] = dataframe.mul(other=28.3495231)
        else: return 
        return self.dataframe

    ## Distance unit ## 
    def distanceConversion(self):
        super().runCleaner()
        currentUnit = self.header.header_preference.current_type
        expectedUnit = self.header.header_preference.desired_type
        name = self.header.name
        dataframe = self.dataframe[name]
        if (currentUnit == "KM") and (expectedUnit == "MI"):
            self.dataframe[name] = dataframe.mul(other=1.60934)
        elif (currentUnit == "MI") and (expectedUnit == "KM"):
            self.dataframe[name] = dataframe.div(other=1.60934)
            
        if (currentUnit == "Meter") and (expectedUnit == "Feet"):
            self.dataframe[name] = dataframe.mul(other=3.281)
        elif (currentUnit == "Feet") and (expectedUnit == "Meter"):
            self.dataframe[name] = dataframe.div(other=3.281)
            
        if (currentUnit == "Centimeter") and (expectedUnit == "Inch"):
            self.dataframe[name] = dataframe.div(other=2.54)
        elif (currentUnit == "Inch") and (expectedUnit == "Centimeter"):
            self.dataframe[name] = dataframe.mul(other=2.54)
        else: return 
        return self.dataframe
