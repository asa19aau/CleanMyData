#Module base class from which all other modules will derive from
from manager.standardMethods.cleanMyDataSTDFunc import *
from datetime import datetime

class Module:
    def __init__(self, header, dataframe):
        self.dataframe = dataframe
        self.header = header

    def runCleaner(self):
        name = self.header.name
        if self.header.is_num == True:
            pref = self.header.header_preference.null_choice_num
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe, [name])
                print(f"removing tuples on column {header.name}")
            elif pref == 'Avg':
                self.dataframe[name] = replaceNullWithAverage(self.dataframe[name])
            elif pref == 'Med':
                self.dataframe[name] = replaceNullWithMedian(self.dataframe[name])
            elif pref == 'Min':
                self.dataframe[name] = replaceNullWithValue(self.dataframe[name], getMinimumValue(self.dataframe[name]))
            elif pref == 'Max':
                self.dataframe[name] = replaceNullWithValue(self.dataframe[name], getMaximumValue(self.dataframe[name]))
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass
        elif self.header.is_string == True:
            pref = self.header.header_preference.null_choice_string
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe, [name])
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass
        elif self.header.is_date == True:
            pref = self.header.header_preference.null_choice_date
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe, [name])
            elif pref == 'Now':
                self.dataframe[name] = replaceNullWithValue(self.dataframe[name], datetime.now())
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass
        return self.dataframe


    #This class is responsible for the communication between modules and the rest of the system#
    def generalModulesMethod():
        return
