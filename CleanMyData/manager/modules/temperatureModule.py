from re import A
import pyspark.pandas as pan

#Only works if temperature is in celcius

def minimumTemperatureConstraint(dataFrame: pan.DataFrame):
    minTemp = (-273.15)
    df = dataFrame.where(dataFrame > minTemp)
    return df.dropna(axis=0)

def TemperatureClimateRangeConstraint(dataFrame: pan.DataFrame, climateZoneLabel: str, temperatureLabel: str):
    df = dataFrame.where((dataFrame[climateZoneLabel] == "Polar") and (dataFrame[temperatureLabel] > 10), dataFrame = None)
    df = df.where((df[climateZoneLabel] == "Tropical") and (df[temperatureLabel] < 22), df = None)
    return df.dropna(axis=0)




