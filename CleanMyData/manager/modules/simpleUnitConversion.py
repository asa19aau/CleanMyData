import pyspark.pandas as pan

## Temperature unit ##
def temperatureConversion(dataFrame: pan.DataFrame, currentUnit: str, expectedUnit: str):
    if (currentUnit == "Celsius") and (expectedUnit == "Fahrenheit"): 
        return dataFrame.mul(other=9/5).add(other=32)
    elif (currentUnit == "Celsius") and (expectedUnit == "Kelvin"): 
        return dataFrame.add(other=273.15)

    elif (currentUnit == "Fahrenheit") and (expectedUnit == "Celsius"): 
        return dataFrame.sub(other=32).mul(other=(5/9))
    elif (currentUnit == "Fahrenheit") and (expectedUnit == "Kelvin"): 
        df = dataFrame.sub(other=32).mul(other=(5/9))
        return df.add(other=275.15)  

    elif (currentUnit == "Kelvin") and (expectedUnit == "Celsius"): 
        return dataFrame.sub(other=273.15)
    elif (currentUnit == "Kelvin") and (expectedUnit == "Fahrenheit"): 
        df = dataFrame.sub(other=275.15)
        return df.mul(other=9/5).add(other=32)
    else: return

## Weight unit ##
def weightConversion(dataFrame: pan.DataFrame, currentUnit: str, expectedUnit: str):
    if (currentUnit == "Kilogram") and (expectedUnit == "Pound"):
        return dataFrame.mul(other=2.20462262)
    elif (currentUnit == "Pound") and (expectedUnit == "Kilogram"):
        return dataFrame.mul(other=0.45359237)
        
    elif (currentUnit == "Gram") and (expectedUnit == "Ounce"):
        return dataFrame.mul(other=0.0352739619)
    elif (currentUnit == "Ounce") and (expectedUnit == "Gram"):
        return dataFrame.mul(other=28.3495231)
    else: return 

## Distance unit ## 
def distanceConversion(dataFrame: pan.DataFrame, currentUnit: str, expectedUnit: str):
    if (currentUnit == "Kilometer") and (expectedUnit == "Mile"):
        return dataFrame.mul(other=1.60934)
    elif (currentUnit == "Mile") and (expectedUnit == "Kilometer"):
        return dataFrame.div(other=1.60934)
        
    if (currentUnit == "Meter") and (expectedUnit == "Feet"):
        return dataFrame.mul(other=3.281)
    elif (currentUnit == "Feet") and (expectedUnit == "Meter"):
        return dataFrame.div(other=3.281)
        
    if (currentUnit == "Centimeter") and (expectedUnit == "Inch"):
        return dataFrame.div(other=2.54)
    elif (currentUnit == "Inch") and (expectedUnit == "Centimeter"):
        return dataFrame.mul(other=2.54)
    else: return 