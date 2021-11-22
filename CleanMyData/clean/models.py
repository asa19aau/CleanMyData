from django.db import models

class Cleaner(models.Model):
    id = models.AutoField(primary_key=True)
    
    # Preferences goes here
    remove_null_values = models.BooleanField(default=True)
    
    # Url API goes here
    
    file = models.FileField(upload_to="media", null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
