from django.db import models
import json
from .validators import validate_file_extension
import os


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
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="headers")
    
    selected = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} | Selected: {self.selected}"
    

class HeaderPreference(models.Model):
    id = models.AutoField(primary_key=True)
    
    header = models.OneToOneField(Header, on_delete=models.CASCADE, related_name='header_preference')
    
    DATA_CHOICES = [
        ('non', 'None'),
        ('Temperature', (
                ('C', 'Celsius'),
                ('F', 'Fahrenheit'),
                ('K', 'Kelvin'),
            )
        ),
        ('Distance', (
                ('KM', 'Kilometer'),
                ('MI', 'Mile'),
            )
        ),
        ('Weight', (
                ('KG', 'Kilogram'),
                ('LB', 'Pound')
            )
        ),
    ]

    current_type = models.CharField(
        max_length = 3,
        choices = DATA_CHOICES,
        default = 'non'
    )
    
    desired_type = models.CharField(
        max_length = 3,
        choices = DATA_CHOICES,
        default = 'non'
    )
    
    def __str__(self):
        return f"{id}"