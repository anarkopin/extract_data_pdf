from django.db import models
from simple_history.models import HistoricalRecords


class TaxFiling(models.Model):
    identificador = models.CharField(max_length=255)
    tax_filing = models.CharField(max_length=255)
    wages = models.IntegerField( )
    total_deductions = models.IntegerField()
    history = HistoricalRecords()
