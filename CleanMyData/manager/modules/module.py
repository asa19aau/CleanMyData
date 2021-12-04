#Module base class from which all other modules will derive from
from manager.standardMethods.cleanMyDataSTDFunc import *
from datetime import datetime

class Module:
    def __init__(self, header, dataframe):
        self.dataframe = dataframe
        self.header = header

    def runCleaner(self):
        if header.is_num == True:
            pref = self.header.header_preference.null_choice_num
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe)
            elif pref == 'Avg':
                self.dataframe = replaceNullWithAverage(self.dataframe)
            elif pref == 'Med':
                self.dataframe = replaceNullWithMedian(self.dataframe)
            elif pref == 'Min':
                self.dataframe = replaceNullWithValue(self.dataframe, getMinimumValue(self.dataframe))
            elif pref == 'Max':
                self.dataframe = replaceNullWithValue(self.dataframe, getMaximumValue(self.dataframe))
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass
        elif header.is_string == True:
            pref = selfheader.header_preference.null_choice_string
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe)
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass
        elif header.is_date == True:
            pref = self.header.header_preference.null_choice_date
            if pref == 'remove-tuples':
                self.dataframe = deleteNullValues(self.dataframe)
            elif pref == 'Now':
                self.dataframe = replaceNullWithValue(self.dataframe, datetime.now())
            elif pref == 'Cus':
                pass
            elif pref == 'nothing':
                pass


    #This class is responsible for the communication between modules and the rest of the system#
    def generalModulesMethod():
        return
