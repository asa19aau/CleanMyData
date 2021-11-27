import pyspark.pandas as pan, standardMethods.average
from CleanMyData.manager.modules.module import Module

class TemperatureModule(Module):
#Only functions if temperature is in celcius

    def minimumTemperatureConstraint(dataFrame: pan.DataFrame):
        minTemp = (-273.15)
        df = dataFrame.where(dataFrame > minTemp)
        return df.dropna(axis=0)

    def temperatureClimateRangeConstraint(dataFrame: pan.DataFrame, climateZoneLabel: str, temperatureLabel: str):
        df = dataFrame.where(((dataFrame[climateZoneLabel] == 'Polar') and (dataFrame[temperatureLabel] > 10) 
        or (dataFrame[climateZoneLabel] == 'Tropical') and (dataFrame[temperatureLabel] < 22)), other=None)
        return df.fillna(value=standardMethods.average.calculateAverage(dataFrame), axis=0)

    def removeUnwantedCountries(dataFrame: pan.DataFrame, countryLabel, unwantedCountry):
        df = dataFrame.where(dataFrame[countryLabel] == unwantedCountry, other=None)
        return df.dropna(axis=0)

    def removeTemperatureUncertainty(dataFrame: pan.DataFrame, uncertantyLabel, acceptableUncertainty: int):
        df = dataFrame.where(dataFrame[uncertantyLabel] > acceptableUncertainty, other=None)
        return df.dropna(axis=0)







