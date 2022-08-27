from secrets import choice
from django.db import models
from datetime import datetime

# Create your models here.
class Ethanol(models.Model):
    IdNo = models.BigAutoField(primary_key=True)
    Year = models.PositiveSmallIntegerField(blank=False, null=False)
    Month = models.CharField(max_length=10, blank=False, null=False)
    Product = models.CharField(max_length=30, blank=True, null=True)
    Date = models.DateField(null=True,blank=True)
    REGION = models.CharField(max_length=20, blank=True, null=True)
    COUNTRY = models.CharField(max_length=40, blank=True, null=True)
    EXPORTER = models.CharField(max_length=200, blank=True, null=True)
    IMPORTER = models.CharField(max_length=200, blank=True, null=True)
    QTYMT = models.DecimalField(
        max_digits=25, decimal_places=2, blank=True, default=0.0, null=True)
    StorageType = models.CharField(max_length=25, blank=True, null=True)
    MTonPrice = models.DecimalField(max_digits=8,decimal_places=2,blank=True, default=0.0, null=True)
    VALUEUSD = models.DecimalField(max_digits=20, decimal_places=2, blank=True, default=0.0, null=True)
    
    # def get_absolute_url(self):
    #     return "/"  
        
    
