from django.db import models
import json
from .validators import validate_file_extension
import os
from .choices import *


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="media", null=True, blank=False, validators=[validate_file_extension])
    
    @property
    def file_name(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]
    
    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1]  # [0] returns path+filename
    
    @property
    def file_path(self):
        return self.file.path

    

class Header(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.TextField()
    type = models.TextField()
    file = models.ForeignKey(File, on_delete=models.CASCADE, 
        related_name="headers")
    
    selected = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} | Selected: {self.selected}"

    @property
    def is_num(self):
        # Include more checks once we know the different data types
        return self.type == 'number'
    
    @property
    def is_string(self):
        # Include more checks once we know the different data types
        return self.type == 'string'

    @property
    def is_date(self):
        # Include more checks once we know the different data types
        return self.type == 'date'

class HeaderPreference(models.Model):
    id = models.AutoField(primary_key=True)
    
    header = models.OneToOneField(Header, on_delete=models.CASCADE, 
        related_name='header_preference')
    
    null_choice_num = models.CharField(
        max_length = 20,
        null = True,
        choices = NULL_CHOICES_NUM,
        default = 'remove-tuples'
    )

    null_choice_string = models.CharField(
        max_length = 20,
        null = True,
        choices = NULL_CHOICES_STRING,
        default = 'remove-tuples'
    )

    null_choice_date = models.CharField(
        max_length = 20,
        null = True,
        choices = NULL_CHOICES_DATE,
        default = 'remove-tuples'
    )

    current_type = models.CharField(
        max_length = 3,
        null = True,
        choices = DATA_CHOICES,
        default = 'NON'
    )
    
    desired_type = models.CharField(
        max_length = 3,
        null = True,
        choices = DATA_CHOICES,
        default = 'NON'
    )
    
    def __str__(self):
        return "ID: " + str(self.id) + " | HEADER: " + self.header.name + " | CURRENT: " + self.current_type + " | DESIRED: " + self.desired_type