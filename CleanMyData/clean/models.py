from django.db import models
import json
from .validators import validate_file_extension
import os
from .choices import *


class Upload(models.Model):
    id = models.AutoField(primary_key=True)

    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"ID: {str(self.id)} | Documents: {str(self.documents.count())}"

    
class Document(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="media", null=False, blank=False, validators=[validate_file_extension])
    is_wrangled = models.BooleanField(default=False)

    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='documents')

    @property
    def file_name(self):
        return os.path.splitext(os.path.basename(self.file.name))[0]
    
    @property
    def file_extension(self):
        return os.path.splitext(self.file.name)[1]  # [0] returns path+filename
    
    @property
    def file_path(self):
        return self.file.path

    def __str__(self):
        return f"ID: {str(self.id)} | File: {self.file_name}{self.file_extension}"


class Header(models.Model):
    id = models.AutoField(primary_key=True)
    
    name = models.TextField()
    type = models.TextField()
    selected = models.BooleanField(default=True)

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="headers")
         
    def __str__(self):
        return f"{self.name} | Selected: {self.selected}"

    @property
    def is_num(self):
        # Include more checks once we know the different data types
        number_types = ['bigint', 'int', 'double']
        return self.type in number_types
    
    @property
    def is_string(self):
        # Include more checks once we know the different data types
        string_types = ['string']
        return self.type in string_types    

    @property
    def is_date(self):
        # Include more checks once we know the different data types
        date_types = ['date']
        return self.type in date_types

    @property
    def is_boolean(self):
        boolean_types = ['boolean']
        return self.type in boolean_types


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