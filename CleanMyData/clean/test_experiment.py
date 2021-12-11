from django.test import TestCase
from .models import File

class TestExperiment(TestCase):
    def setUp(self):
        print("setup")
    
    def test_data_wrangling(self):
        print("test_data_wrangling")
