from django.db import models
import json
from .validators import validate_file_extension
import os

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession



def retrieve_file_columns(file):
    # spark = SparkSession.builder.getOrCreate()
    # df = spark.read.csv('C:/GitHub/P5/P5/CleanMyData/uploads/media/sample2_0xHjPIs.json', header=True)
    # print(df)
    return json.dumps(["Temp", "Length", "PersonNumber", "Name", "PhoneNumber"])


class File(models.Model):
    id = models.AutoField(primary_key=True)
    
    file = models.FileField(upload_to="media", null=True, blank=False, validators=[validate_file_extension])
    
    def __str__(self):
        return str(self.id)
    
    @property
    def file_name(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]
    
    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1]  # [0] returns path+filename



class Preferences(models.Model):
    id = models.AutoField(primary_key=True)
    
    file = models.OneToOneField(File, on_delete=models.CASCADE, related_name="preferences")
    columns = models.JSONField("Preferences", default=retrieve_file_columns(file))
    
    def __str__(self):
        return str(self.id) + " | " + str(self.columns)