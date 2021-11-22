from django.db import models

class Cleaner(models.Model):
    
    NULL_CHOICES = [
        ('DN', 'Do nothing'),
        ('RV', 'Remove values'),
        ('RA', 'Replace with avg.'),
        ('RM', 'Replace with median'),
    ]
    
    id = models.AutoField(primary_key=True)
    
    # General data sheet goes here
    null_values = models.CharField(max_length=2, choices=NULL_CHOICES, default='DN')
    remove_duplicate_rows = models.BooleanField(default=False)
    
    
    # Individual Columns Preferences goes here
    
    # Url API goes here
    
    file = models.FileField(upload_to="media", null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
